# Generated by Django 4.2.2 on 2023-09-13 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0033_remove_checkout_order_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='order_details',
            field=models.ManyToManyField(to='menu.orderdetail'),
        ),
    ]