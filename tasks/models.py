from django.contrib.auth.models import AbstractUser
import datetime
from django.db import models
from django.utils import timezone
from users.models import User

# models for the api



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