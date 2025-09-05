from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)   # renamed
    updated = models.DateTimeField(auto_now=True)       # renamed
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)       # renamed
    created = models.DateTimeField(auto_now_add=True)   # renamed

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:50]  # Return the first 50 characters
