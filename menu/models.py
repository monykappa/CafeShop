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
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filenamecd
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
    SMALL = 'SM'
    MEDIUM = 'MD'
    LARGE = 'LG'

    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'), 
        (LARGE, 'Large'),
    ]

    size = models.CharField(max_length=50, choices=SIZE_CHOICES, null=True, blank=True)
    def __str__(self):
        return self.get_size_display()
    
class AddProduct(models.Model):
    product_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(blank=True, upload_to=menu_directory_path, validators=[validate_file_extension])
    category = models.CharField(max_length=100, choices=category, null=True, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        sizes_str = ", ".join(str(size) for size in self.sizes.all())
        return f"{self.product_name} - Sizes: {sizes_str} - Price: ${self.price:.2f}"

class OrderDetail(models.Model):
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def calculate_total_price(self):
        if self.product is not None:
            price_per_unit = self.product.price # Assuming 'price' is a field in the AddProduct model
            self.total_price = price_per_unit * self.quantity
        else:
            self.total_price = 0.0

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderDetailID: {self.pk} - {self.product.product_name} - Total Price: ${self.total_price:.2f}"
    
