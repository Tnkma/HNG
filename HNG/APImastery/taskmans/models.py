from django.contrib.auth.hashers import make_password
import datetime
from django.db import models
from django.utils import timezone

# models for the api

class User(models.Model):
    """User model representing a user in the system."""
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    
    def save(self, *args, **kwargs):
        """Hash the password before saving to the model."""
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the username of the user."""
        return str(self.username)

class Task(models.Model):
    """Task model representing a task."""
    PRIORITY = [
        ("L", "Low"),
        ("H", "High"),
        ("M", "Medium")
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=1, choices=PRIORITY)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assignedTo = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)
    tags = models.JSONField()

    class Meta:
        """Meta class for indexing the database."""
        indexes = [
            models.Index(fields=['created_by', 'title', 'created_at', 'due_date']),
        ]

    def __str__(self):
        """Return a string representation of the task."""
        return f'{self.title} - {self.description} - Due: {self.due_date} - Status: {self.status}'

    def was_created_recently(self):
        """Return True if the task was created recently."""
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    def was_updated_recently(self):
        """Return True if the task was updated recently."""
        return self.updated_at >= timezone.now() - datetime.timedelta(days=1)
