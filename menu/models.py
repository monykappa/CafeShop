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


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def calculate_total_price(self):
        if self.product_size is not None:
            price_per_unit = self.product_size.price
            return price_per_unit * self.quantity
        return 0.0


class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, null=True)
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
        product_size = self.product_size
        if product_size and product_size.product:
            return f"OrderDetailID: {self.pk} - {product_size.product.product_name} - Quantity: {self.quantity} - Total Price: ${self.total_price:.2f}"
        else:
            return f"OrderDetailID: {self.pk} - Product: N/A - Quantity: {self.quantity} - Total Price: ${self.total_price:.2f}"



class OrderItem(models.Model):
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"OrderItem ID: {self.pk} - Product: {self.product_size.product.product_name} - Quantity: {self.quantity}"


class Checkout(models.Model):
    checkout_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem, related_name='checkouts', blank=True)
    order_date = models.DateTimeField(auto_now_add=True, null=True)  # Automatically record the order date

    def __str__(self):
        return f"Checkout ID {self.checkout_id}"



