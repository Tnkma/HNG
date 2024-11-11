from rest_framework import status, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer, TaskTagsSerializer
from django.core.mail import send_mail
from django.conf import settings

class UserSignup(APIView):
    """View for creating a new user."""
    permission_classes = []
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Email subject and message
        subject = 'New User Signed Up'
        message = (
            f"A new user has signed up:\n\n"
            f"Name: {user.username}\n"
            f"Email: {user.email}\n\n"
            "Login to the admin panel to view more details."
        )
        
        # Send the email to the new user
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class UserLogin(APIView):
    """View for logging in a user."""
    permission_classes = []
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        
        if not user or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

@method_decorator(cache_page(60), name='dispatch')
class UserDetail(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

@method_decorator(cache_page(60), name='dispatch')
class TaskList(ListAPIView):
    """View for listing tasks."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class TaskCreate(APIView):
    """View for creating a task."""
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(cache_page(60), name='dispatch')
class TaskDetail(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a task."""
    serializer_class = TaskSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        return Task.objects.filter(createdBy=self.request.user.id)

@method_decorator(cache_page(60), name='dispatch')
class TaskSearch(ListAPIView):
    """View for searching tasks."""
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'description', 'status', 'createdBy', 'AssignedTo', 'dueDate']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(createdBy=user) | Task.objects.filter(AssignedTo=user)

class Logout(APIView):
    """View for logging out a user."""
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            RefreshToken(refresh_token).blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class TagView(APIView):
    """View for adding and removing tags from a task."""
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Add a tag to a task, creating the tag if it doesn't exist."""
        task_id = request.data.get('task')
        tag_name = request.data.get('name')
        
        try:
            task = Task.objects.get(id=task_id)
            
            # Ensure the user is the task's creator
            if task.createdBy != request.user:
                raise PermissionDenied("You do not have permission to modify tags for this task.")
            
            # Check if the tag already exists on the task
            tag, created = TaskTagsSerializer.objects.get_or_create(name=tag_name)
            if task.tags.filter(id=tag.id).exists():
                return Response({
                    'message': 'Tag already exists on this task.',
                    'tag': TaskTagsSerializer(tag).data
                }, status=status.HTTP_200_OK)
            
            # Otherwise, add the new tag
            task.tags.add(tag)
            return Response({
                'message': 'Tag added successfully',
                'tag': TaskTagsSerializer(tag).data
            }, status=status.HTTP_201_CREATED)
        
        except Task.DoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)