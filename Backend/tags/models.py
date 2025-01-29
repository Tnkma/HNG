""" Models for Tags and AssignedTo"""
from django.db import models
from users.models import User
from tasks.models import Task

# models for the api
    
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
