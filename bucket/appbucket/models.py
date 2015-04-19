from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from taggit.managers import TaggableManager

class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    completed_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User)
    tags = TaggableManager()

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=20, blank=True)

def user_post_save(sender, instance=None, created=False, **kwargs):
    if instance is not None and created:
        Profile.objects.create(user=instance)

post_save.connect(user_post_save, sender=User)
