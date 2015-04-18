from django.db import models
from datetime import datetime


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    createdDate = models.DateTimeField(default=datetime.now)
    completedDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
