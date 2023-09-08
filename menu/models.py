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
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def menu_directory_path(instance, filename):
    unique_id = str(uuid.uuid4())
    directory_path = f'content/{unique_id}/'
    return os.path.join(directory_path, filename)

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

class Image(models.Model):
    image = models.FileField(upload_to=menu_directory_path, validators=[validate_file_extension])

    def __str__(self):
        return f"ImageID: {self.pk}"

class AddProduct(models.Model):
    CATEGORY_CHOICES = [
        ('Coffee', 'Coffee'),
        ('Tea', 'Tea'),
        ('Soda', 'Soda'),
        ('Milk', 'Milk'),
    ]
    product_name = models.CharField(max_length=100, null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        sizes_str = ", ".join(str(size) for size in self.sizes.all())
        return f"{self.product_name} - Sizes: {sizes_str} - Price: ${self.price:.2f}"

class OrderDetail(models.Model):
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def calculate_total_price(self):
        if self.product is not None:
            price_per_unit = self.product.price
            self.total_price = price_per_unit * self.quantity
        else:
            self.total_price = 0.0

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super(OrderDetail, self).save(*args, **kwargs)

    def __str__(self):
        return f"OrderDetailID: {self.pk} - {self.product.product_name} - Total Price: ${self.total_price:.2f}"

    def get_product_images(self):
        if self.product is not None:
            return self.product.images.all()
        return None
    
