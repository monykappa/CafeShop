# Generated by Django 4.2.2 on 2023-09-14 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_checkout_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='OrderItem',
            new_name='orderitem',
        ),
    ]
