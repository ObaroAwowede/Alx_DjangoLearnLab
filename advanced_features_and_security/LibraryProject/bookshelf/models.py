from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields): 
        if not username:
            raise ValueError('Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields): 
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True) 
    profile_photo = models.ImageField(upload_to='profile_photo/', null=True, blank=True)
    objects = CustomUserManager()
    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    publication_year = models.IntegerField(default = 1900)

    class Meta:
        permissions = [
            ("can_view_book", "Can view book"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"