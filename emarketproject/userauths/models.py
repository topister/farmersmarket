from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import unique
from django.db.models.signals import post_save
from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model
# User = get_user_model()


# Create your models here.
from userauths.managers import CustomUserManager

JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)


# class User(AbstractUser):
#     email =models.EmailField(unique=True)
#     username = models.CharField(max_length=100)
#     bio = models.CharField(max_length=100)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['username']

#     role = models.CharField(choices=ROLE,  max_length=10)
#     # gender = models.CharField(choices=JOB_TYPE, max_length=1)
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
#     # gender = models.CharField(choices=JOB_TYPE, max_length=1, blank=True, null=True)


#     def __str__(self):
#         return self.username
    
#     def __str__(self):
#         return self.email
    
#     def get_full_name(self):
#         return self.first_name+ ' ' + self.last_name
    
#     objects = CustomUserManager()
  
    
 



from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from userauths.managers import CustomUserManager

JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('admin', "Admin"),
    ('employer', "Employer"),
    ('employee', "Employee"),

)

class User(AbstractUser):
    # username = None
    is_author = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpeg")

    username = models.CharField(max_length=100)
    # username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    bio = models.CharField(max_length=100)
    role = models.CharField(choices=ROLE,  max_length=10)
    # gender = models.CharField(choices=JOB_TYPE, max_length=1)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    # gender = models.CharField(choices=JOB_TYPE, max_length=1, blank=True, null=True)

    USERNAME_FIELD = "email"
    # USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    # def __str__(self):
    #     return self.username

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    image = models.ImageField(upload_to='profile/')
    fullname = models.CharField(max_length=100)
    bio = models.CharField(max_length=256, blank=True)
    phone  = models.CharField(max_length=100)
    verified = models.BooleanField(default= False)


    def  __str__(self):
       return self.user.username
    
    # def __str__(self):
    #     try:
    #         return self.fullname
    #     except: 
    #         return self.user.username
 

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

 
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User) 

