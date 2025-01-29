from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from tasks.models import Task
from tags.serializers import TaskTagsSerializer
from rest_framework import status



class TagView(APIView):
    """View for adding and removing tags from a task."""
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Add a tag to a task, creating the tag if it doesn't exist."""
        serializer = TaskTagsSerializer(data=request.data)
        
        if serializer.is_valid():
            task_id = serializer.validated_data('user')
            tag_name =serializer.validated_data('name')
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