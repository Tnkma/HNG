from rest_framework import serializers
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_full_name(self, obj):
        """Return the full name of the user."""
        return f'{obj.email} {obj.username}'

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""
    
    createdBy = UserSerializer(read_only=True)
    assignedTo = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Override create method to handle task creation."""
        # Extract user data from the validated_data if needed
        created_by_data = validated_data.pop('createdBy')
        assigned_to_data = validated_data.pop('assignedTo')

        # Create task instance
        task = Task.objects.create(**validated_data, createdBy=created_by_data, assignedTo=assigned_to_data)

        return task
