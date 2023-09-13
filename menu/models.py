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
from django.core.validators import RegexValidator
from userprofile.models import Customer

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
    category = models.CharField(max_length=100, choices=category, null=True, blank=True)

    def __str__(self):
        return self.product_name

class ProductSize(models.Model):
    product = models.ForeignKey(AddProduct, related_name='sizes', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, null=True, blank=True)
    images = models.FileField(upload_to=menu_directory_path, validators=[validate_file_extension], blank=True)

    def __str__(self):
        return f"{self.product.product_name} - Size: {self.size.get_size_display()} - Price: ${self.price:.2f}"

class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_time = models.DateTimeField(default=timezone.now)

    def calculate_total_price(self):
        if self.product_size is not None:
            price_per_unit = self.product_size.price
            self.total_price = price_per_unit * self.quantity
        else:
            self.total_price = 0.0

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderDetailID: {self.pk} - {self.product_size.product.product_name} - Quantity: {self.quantity} - Total Price: ${self.total_price:.2f}"


class Order(models.Model):
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order ID: {self.pk} - Product: {self.order_detail.product_size.product.product_name} - Quantity: {self.order_detail.quantity}"

    def calculate_total_price(self):
        return self.order_detail.total_price

    def save(self, *args, **kwargs):
        self.order_detail.calculate_total_price()  # Recalculate total price if needed
        super().save(*args, **kwargs)

class Checkout(models.Model):
    checkout_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    order_details = models.ManyToManyField(OrderDetail)
    order = models.ManyToManyField(Order)

    def __str__(self):
        return f"Checkout ID: {self.checkout_id}"

    def calculate_total_price(self):
        total_price = 0
        for order_detail in self.order_details.all():
            total_price += order_detail.total_price
        return total_price


