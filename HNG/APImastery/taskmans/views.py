""" This file is used to define the views for the taskmans app. """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer

# testing the concrete generic view here
class UserList(ListCreateAPIView):
    """ Concrete generic view for listing users and creating new users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Trottle classes assigns the rate limit to the user and anonymous user
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class UserDetail(RetrieveUpdateDestroyAPIView):
    """ Concrete generic view for retrieving, updating and deleting a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Trottle classes assigns the rate limit to the user and anonymous user
    throttle_classes = [UserRateThrottle, AnonRateThrottle]