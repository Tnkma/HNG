from rest_framework import serializers
from .models import User, Task, TaskTags, AssignedTo

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    # full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }
        
class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""
    
    createdBy = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['title','description', 'due_date', 'status', 'createdAt', 'updatedAt', 'priority', 'createdBy']
        read_only_fields = ['createdBy', 'createdAt', 'updatedAt']

class TaskTagsSerializer(serializers.ModelSerializer):
    """Serializer for the TaskTags model."""
    
    name = serializers.CharField(max_length=50)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    
    class Meta:
        model = TaskTags
        fields = ['name', 'task']


class AssignedToSerializer(serializers.ModelSerializer):
    """Serializer for the AssignedTo model."""
    
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    
    class Meta:
        model = AssignedTo
        fields = ['user', 'task']