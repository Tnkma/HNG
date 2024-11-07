""" This file is used to define the views for the taskmans app. """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.core.cache import cache
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer

class UserSignup(CreateAPIView):
    """Concrete generic view for creating a new user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
# class UserSignin()

class UserDetail(RetrieveUpdateDestroyAPIView):
    """Concrete generic view for retrieving, updating and deleting a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Permission classes to check if the user is authenticated before they can make changes
    permission_classes = [IsAuthenticated]
    

    # Throttle classes assign the rate limit to both auth.user and anonymous user
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    # We want Users to be able to only update their own details
    def get_queryset(self):
        """ Override to filter the queryset by the user id. """
        return super().get_queryset().filter(id=self.request.user.id)

    # Check for cache and return the user detail
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

class TaskList(ListCreateAPIView):
    """ Concrete generic view for listing tasks and creating new tasks. """
    # queryset and serializer for the serializer class
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # Any user can see all the tasks but only authenticated users can create a task
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Throttle classes assign the rate limit to the user and anonymous user requests
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    # Allow createdBy to be set to the current user
    def perform_create(self, serializer):
        """ Override to set the createdBy field to the current user. """
        serializer.save(createdBy=self.request.user)
    
    
    # Check for cache and return the task list
    
class TaskDetail(RetrieveUpdateDestroyAPIView):
    """ Concrete generic view for retrieving, updating and deleting a task. """
    # queryset and serializer for the serializer class
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # only authn users can update and destroy a task
    permission_classes = [IsAuthenticated]

    # Throttle classes assign the rate limit to the user and anonymous user requests
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    # We want Users to be able to only update their own task
    def get_queryset(self):
        """ Override to filter the queryset by the user id. """
        return Task.objects.filter(createdBy=self.request.user.id)
    
    # Check for cache and return the task detail
