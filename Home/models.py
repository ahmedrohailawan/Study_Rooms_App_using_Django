from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default="avatar.svg")
    is_online = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  []


class Topic(models.Model):
    name = models.CharField(max_length=122)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Room(models.Model):    
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    topics = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=122)
    description = models.TextField(max_length=250,null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.body[0:50]

