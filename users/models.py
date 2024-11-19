from django.contrib.auth.models import AbstractUser
import datetime
from django.db import models
from django.utils import timezone

# models for the api

class User(AbstractUser):
    """User model representing a user in the system."""
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, blank=False)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    def __str__(self):
        """Return the username of the user."""
        return str(self.username)
