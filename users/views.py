from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserSerializer
from APImastery.redis_client import redis_client
from rest_framework.permissions import IsAuthenticated
from redis.exceptions import RedisError


class UserSignup(APIView):
    """View for creating a new user."""
    # permission_classes = []
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUsers(ListAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
        

class UserLogin(APIView):
    """View for logging in a user."""
    # permission_classes = []
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        
        if not user or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            # 'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserDetail(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        """ cache and retrive the user detail"""
        cache_key = f"user_{self.request.user.id}"
        
        # try to get the cache data using the cache key
        try:
            user_data = redis_client.get(cache_key)
            
            if not user_data:
                
                # retrive from the database
                user_data = self.queryset.filter(id=self.request.user.id).first()
                # serialize and store cache for 5 minutes
                if user_data:
                    serializer = UserSerializer(user_data)
                redis_client.set(cache_key, serializer.data, timeout=300)
        except RedisError as err:
            print({"error: {err}"})
        
            # Deserialize back to dic and return
        return UserSerializer(data=user_data)


class Logout(APIView):
    """View for logging out a user."""
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            RefreshToken(refresh_token).blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
