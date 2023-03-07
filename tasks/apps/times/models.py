from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from apps.tasks.models import Task


class Time(models.Model):
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True)
    minutes = models.IntegerField(default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
