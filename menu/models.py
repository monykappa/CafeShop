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

def validate_file_extension(value): 
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def menu_directory_path(instance, filename):
    # Generate a unique identifier for the directory
    unique_id = str(uuid.uuid4())
    # Construct the directory path
    directory_path = f'content/{unique_id}/'
    
    # Return the complete file path
    return os.path.join(directory_path, filename)

category = (
    ('Coffee', 'Coffee'),
    ('Tea', 'Tea'),
    ('Soda', 'Soda'),
    ('Milk', 'Milk'),
)

class Size(models.Model):
    size_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.size_name

class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(blank=True, upload_to=menu_directory_path, validators=[validate_file_extension])  # Wrap in a list
    category = models.CharField(max_length=100, choices=category, null=True, blank=True)

    def __str__(self):
        return self.product_name


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.product.product_name} - {self.size.size_name} - ${self.price:.2f}"

class OrderDetail(models.Model):
    product_price = models.ForeignKey(ProductPrice, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"OrderDetailID: {self.pk} - {self.product_price.product.product_name} - Total Price: ${self.total_price}"