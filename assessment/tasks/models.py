from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Task(models.Model):
    
    STATUS_TYPE_PENDING="PENDING"
    STATUS_TYPE_CANCELLED="CANCELLED"
    STATUS_TYPE_COMPLETED="COMPLETED"
    STATUS_TYPE_OVERDUE="OVERDUE"
    
    STATUS_CHOICES = [
        (STATUS_TYPE_PENDING, STATUS_TYPE_PENDING),
        (STATUS_TYPE_CANCELLED, STATUS_TYPE_CANCELLED),
        (STATUS_TYPE_COMPLETED, STATUS_TYPE_COMPLETED),
        (STATUS_TYPE_OVERDUE, STATUS_TYPE_OVERDUE),
    ]
    
    title=models.CharField(max_length=50)
    
    description= models.TextField()

    user=models.ForeignKey(User, related_name='created_tasks',on_delete=models.CASCADE)

    status=models.CharField(max_length=15, choices=STATUS_CHOICES)
    due=models.DateTimeField()
