# Generated by Django 4.2.2 on 2023-09-03 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_image_remove_addproduct_image_addproduct_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
