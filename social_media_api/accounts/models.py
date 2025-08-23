from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField()
    followers = models.ManyToManyField("self", symmetrical=False)