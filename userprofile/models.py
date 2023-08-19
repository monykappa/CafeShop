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



class SignUp(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    sex = models.CharField(max_length=7, choices=Sex, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, unique=True)
    password = models.CharField(max_length=128)

    
    def __str__(self):
        return self.username
