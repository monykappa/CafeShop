# Generated by Django 4.2.2 on 2023-09-14 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0072_confirm_quantity_alter_confirm_products_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirm',
            name='quantity',
        ),
    ]
