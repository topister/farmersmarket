from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import unique
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save

# Create your models here.

class User(AbstractUser):
    email =models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def str(self):
        return self.username
    
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/')
    fullname = models.CharField(max_length=100)
    bio = models.CharField(max_length=256, blank=True)
    phone  = models.CharField(max_length=100)
    verified = models.BooleanField(default= False)


    def  __str__(self):
       return self.user.username
 

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

 
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User) 


