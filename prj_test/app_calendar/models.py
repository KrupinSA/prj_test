from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TaskCalendar(models.Model):
   title = models.CharField(max_length=250)
   description = models.TextField()
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_tasks')
   date = models.DateTimeField()
   status = models.BooleanField(default=False)