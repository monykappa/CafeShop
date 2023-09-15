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
import uuid






Sex = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

DistrictChoices = (
    ("Khan Boeng Keng Kang", "Khan Boeng Keng Kang"),
    ("Doun Penh section", "Doun Penh section"),
    ("Khan Kamboul", "Khan Kamboul"),
    ("Khan Chamkar Mon", "Khan Chamkar Mon"),
    ("Khan Chbar Ampov", "Khan Chbar Ampov"),
    ("Khan Chroy Changvar", "Khan Chroy Changvar"),
    ("Khan Dangkao", "Khan Dangkao"),
    ("Khan Mean Chey", "Khan Mean Chey"),
    ("Khan Pou Senchey", "Khan Pou Senchey"),
    ("Khan Prampir Makara", "Khan Prampir Makara"),
    ("Khan Russey Keo", "Khan Russey Keo"),
    ("Khan Sen Sok", "Khan Sen Sok"),
    ("Khan Tuol Kouk", "Khan Tuol Kouk"),
    ("Khan Prek Pnov", "Khan Prek Pnov"),
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(
        max_length=50,
        choices=DistrictChoices,
        null=True,
        blank=True,
    )
    house_number = models.CharField(max_length=10, null=True, blank=True)
    road = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username



def validate_file_extension(value): 
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filenamecd
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def user_directory_path(instance, filename):
    # Generate a unique identifier for the directory
    unique_id = str(uuid.uuid4())
    # Construct the directory path
    directory_path = f'content/{unique_id}/'
    
    # Return the complete file path
    return os.path.join(directory_path, filename)

class CustomerUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True, null=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=False)
    sex = models.CharField(max_length=7, choices=Sex, null=True, blank=True)
    profile_image = models.ImageField(upload_to=user_directory_path, validators=[validate_file_extension], blank=True)

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
    

    
