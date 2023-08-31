from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
import uuid
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.

Sex = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=7, choices=Sex, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username

class SignUp(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, unique=True)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=7, choices=Sex, null=True, blank=True)

    def __str__(self):
        return self.user.username

