""" Serializers for the taskmans app api """
# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User, Task


class UserSerializer(serializers.ModelSerializer):
    """ User Serializer """
    class Meta:
        """ serializer for the user model """
        model = User
        fields = ['id', 'email', 'username', 'password']
        
        def return_names(self, obj):
            """ returns the names of the user """
            return f'{obj.email} {obj.username}'

class TaskSerializer(serializers.ModelSerializer):
    """ Task Serializer"""
    class Meta:
        """ serializer for the task model """
        model = Task
        fields = '__all__'
        read_only_fields = ['createdBy', 'createdAt', 'updatedAt']
