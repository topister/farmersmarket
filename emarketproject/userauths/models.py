from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email =models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def str(self):
        return self.username