""" Users serializer"""
from rest_framework import serializers
from users.models import User



class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    # full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }
    
    def create(self, validated_data):
        """ Hash the passowrd before saving the user. """
        user = User(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user