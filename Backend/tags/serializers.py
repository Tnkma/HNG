""" serializers"""
from rest_framework import serializers
from users.models import User
from tasks.models import Task
from tags.models import TaskTags, AssignedTo


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