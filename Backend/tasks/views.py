from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from APImastery.redis_client import redis_client
from django.db.models import Q
from django.db.utils import DatabaseError
from redis.exceptions import RedisError



class TaskList(ListAPIView):
    """View for listing tasks."""
    # on home, you will see the list of task created or assigned to you
    # we can also allow user accept certain task to or decline
    # we might also share the task via messages or email.
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
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
class TaskDetail(APIView):
    """Retrieve, update or delete a task."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        
        # try and get from redis
        
        task = Task.objects.filter(
                id=task_id,
                AssignedTo=request.user
                ).first()
        if not task:
            task = Task.objects.filter(
                        id=task_id,
                        createdBy=task_id
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
            #cache.delete(f"task_{task_id}")
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, *args, **kwargs):
        # Similar to PUT, handle partial updates
        return self.put(request, *args, **kwargs)


class TaskSearch(ListAPIView):
    """View for searching tasks."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # only is_authen users can search for tasks
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'description', 'status', 'createdBy', 'AssignedTo', 'dueDate']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    
    def get_queryset(self):
        """ retrive Tasklist from redis first before db"""
        user = self.request.user
        
        cache_key = f"user{user.id}_tasks"
        # get the task createdBY and task AssignedTo
        
        # try to get from redis
        try:
            task_data = redis_client.get(cache_key)
            if task_data:
                # deserialize data
                task_data = TaskSerializer(data=task_data, many=True).data
        except RedisError as err:
            # Log the Redis error (optional)
            print(f"Redis error: {err}")
        
        try:
            # get from the database
            task_data = self.queryset.filter(Q(createdBy=user) | Q(AssignedTo=user))
            # cache the task_data
            if task_data:
                serilaizer = TaskSerializer(task_data, many=True).data
                redis_client.set(cache_key, serilaizer, timeout=300)
            else:
                return Response({'details': 'No Task found for this user'}, status=404)
        except DatabaseError as dataerr:
            # log the database error
            print(f"Database: {dataerr}")
        return task_data