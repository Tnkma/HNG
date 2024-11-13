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

class Task(models.Model):
    """Task model representing a task."""
    PRIORITY = [
        ("L", "Low"),
        ("H", "High"),
        ("M", "Medium")
    ]
    
    # Status of the task
    STATUS = [
        ("P", "Pending"),
        ("C", "Completed"),
        ("I", "In Progress"),
    ]
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=1, choices=PRIORITY)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    # Index database
    class Meta:
        """Meta class for indexing the database."""
        indexes = [
            models.Index(fields=['createdBy', 'title', 'createdAt', 'due_date']),
        ]
    
    def save(self, *args, **kwargs):
        """Override the save method to update the updated time."""
        if self.pk is not None:
            existing_task = Task.objects.get(pk=self.pk)
            if self.title != existing_task.title or self.description != existing_task.description:
                self.updatedAt = timezone.now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the task."""
        return f'{self.title} - {self.description} - Due: {self.due_date} - Status: {self.status}'

    def was_created_recently(self):
        """Return True if the task was created recently."""
        return self.createdAt >= timezone.now() - datetime.timedelta(days=1)

    def was_updated_recently(self):
        """Return True if the task was updated recently."""
        return self.updatedAt >= timezone.now() - datetime.timedelta(days=1)
    
class TaskTags(models.Model):
    """Task tag model representing a tag for a task."""
    name = models.CharField(max_length=50, unique=True)
    task = models.ManyToManyField(Task, related_name='tags')
    
    def __str__(self):
        """Return a string representation of the tag."""
        return self.name

class AssignedTo(models.Model):
    """ Assigns a Task to a User"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        """ Meta class for indexing the database."""
        indexes = [
            models.Index(fields=['task', 'user']),
        ]
        # A task can only be assigned to a user once
        unique_together = ['task', 'user']
    
    def __str__(self):
        """Return a string representation of the assigned task."""
        return f'{self.task} - {self.user}'
