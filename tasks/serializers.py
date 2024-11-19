""" serializer"""
from rest_framework import serializers
from users.serializers import UserSerializer
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""
    
    createdBy = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id','title','description', 'due_date', 'status', 'createdAt', 'priority', 'createdBy']
        read_only_fields = ['createdBy', 'createdAt']
