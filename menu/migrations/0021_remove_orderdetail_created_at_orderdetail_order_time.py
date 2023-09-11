# Generated by Django 4.2.2 on 2023-09-10 09:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0020_orderdetail_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='created_at',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]