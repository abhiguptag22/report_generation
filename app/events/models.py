

# Create your models here.
from django.db import models

class Task(models.Model):
    TASK_TYPES = [('html', 'HTML'), ('pdf', 'PDF')]
    task_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='PENDING')
    result = models.TextField(null=True, blank=True)
    task_type = models.CharField(max_length=10, choices=TASK_TYPES, default='html')


