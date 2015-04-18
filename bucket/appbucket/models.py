from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    createdDate = models.DateTimeField(default=datetime.now)
    completedDate = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title
