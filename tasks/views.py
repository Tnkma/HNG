from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from tasks.models import Task
from tasks.serializers import TaskSerializer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated



@method_decorator(cache_page(60), name='dispatch')
class TaskList(ListAPIView):
    """View for listing tasks."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # All users can view tasks
    permission_classes = []
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class TaskCreate(APIView):
    """View for creating a task."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Cache for 5 minutes
@method_decorator(cache_page(300), name='dispatch')
class TaskDetail(APIView):
    """Retrieve, update or delete a task."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = Task.objects.filter(
                id=task_id,
                assignedto=request.user
                ).first()
        if not task:
            task = Task.objects.filter(
                        id=task_id,
                        created_by=task_id
                        ).first()
            
        if not task:
            return Response({'detail': 'Task not found.'}, status=404)
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = Task.objects.filter(id=task_id).first()
        
        if not task:
            return Response({'detail': 'Task not found.'}, status=404)
        
        # Update the task
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # After update, clear cache for this task so that fresh data is served
            cache.delete(f"task_{task_id}")
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, *args, **kwargs):
        # Similar to PUT, handle partial updates
        return self.put(request, *args, **kwargs)

@method_decorator(cache_page(60), name='dispatch')
class TaskSearch(ListAPIView):
    """View for searching tasks."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # All users can search for tasks
    permission_classes = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'description', 'status', 'createdBy', 'AssignedTo', 'dueDate']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(createdBy=user) | Task.objects.filter(AssignedTo=user)