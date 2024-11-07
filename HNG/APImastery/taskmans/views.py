""" This file is used to define the views for the taskmans app. """
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.core.cache import cache
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserSignup(APIView):
    """ View for creating a new user. """
    permission_classes = []
    
    def post(self, request):
        """ create a new user."""
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class UserLogin(APIView):
    """ View for logging in a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    
    def post(self, request):
        """ check if the user exists and return the user details. """
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        
        # if user not found
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        # Generate a refresh & access token for the user
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(access_token),
        })

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
    """ We allow all vistors to see all the tasks but only authenticated users can create a task """
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
