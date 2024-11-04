""" This file is used to define the views for the taskmans app. """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import User
from .serializers import UserSerializer

class UserList(ListCreateAPIView):
    """Concrete generic view for listing users and creating new users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Throttle classes assign the rate limit to the user and anonymous user
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        """Override to check cache before hitting the database."""
        # define a cache key
        users_cache_key = 'users_list'
        # Get users from the cache
        users = cache.get(users_cache_key)

        # If not found, fetch from the database
        if not users:
            users = super().get_queryset()
            # Cache for 15 minutes
            cache.set(users_cache_key, users, timeout=60*15)

        return users


class UserDetail(RetrieveUpdateDestroyAPIView):
    """Concrete generic view for retrieving, updating and deleting a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Throttle classes assign the rate limit to both auth.user and anonymous user
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_object(self):
        """Override to check cache before hitting the database."""
        # get id using the primary key
        user_id = self.kwargs.get('pk')
        # Create a unique cache key for the user so we can get it later
        user_cache_key = f'user_{user_id}'
        user = cache.get(user_cache_key)

        # If not found, fetch from the database and cache for 15 minutes
        if not user:
            user = super().get_object()
            cache.set(user_cache_key, user, timeout=60*15)

        return user
