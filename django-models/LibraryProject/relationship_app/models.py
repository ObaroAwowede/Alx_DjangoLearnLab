from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    def __str__(self):
        return f"{self.title} by {self.author.name}"
        
    
class Library(models.Model):
    name = models.CharField(max_length = 100)
    books = models.ManyToManyField(Book)
    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length = 100)
    library = models.OneToOneField(
        Library,
        on_delete = models.CASCADE,
        primary_key = True
    )
    def __str__(self):
        return f"{self.name} in {self.library.name}"

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.role})"
