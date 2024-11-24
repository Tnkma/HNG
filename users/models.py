from django.contrib.auth.models import AbstractUser
import datetime
from django.db import models
from django.utils import timezone

# models for the api

class User(AbstractUser):
    """User model representing a user in the system."""
    username = models.CharField(max_length=250, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        """Return the username of the user."""
        return str(self.username)
