""" models for the taskmans app """
import datetime
from django.db import models
from django.utils import timezone


# models for the api

class User(models.Model):
    """ user model """
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=25, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        """ returns the object of the user """
        return str(self.username)


class Task(models.Model):
    """ Task Model """
    PRIORITY = [
        ("L", "Low"),
        ("H", "High"),
        ("M", "Medium")
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    dueDate = models.DateField()
    status = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=1, choices=PRIORITY)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assignedTo = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)
    tags = models.JSONField()


    # indexxing the database to improve the performance
    class Meta:
        """ Meta class for indexing the database"""
        indexes = [
            models.Index(fields=['CreatedBy','title', 'createdAt', 'dueDate']),
        ]


    def __str__(self):
        """ returns the object of the task"""
        return str(self.title, self.description, self.dueDate, self.status, self.createdAt, self.updatedAt, self.priority, self.createdBy, self.assignedTo, self.tags)

    def was_creating_recently(self):
        """ returns the task created recently """
        return self.createdAt >= timezone.now() - datetime.timedelta(days=1)

    def was_updated_recently(self):
        """ returns the task updated recently """
        return self.updatedAt >= timezone.now() - datetime.timedelta(days=1)
