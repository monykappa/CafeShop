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

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.user.username


class CustomerUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True,null=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=False)
    contact = models.CharField(max_length=20, null=True, blank=True)
    sex = models.CharField(max_length=7, choices=Sex, null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Staff(models.Model):
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True)
    dob = models.DateField(null=False)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, unique=True)

    def full_name(self):
        return f"{self.firstname} {self.lastname}"
    

    
