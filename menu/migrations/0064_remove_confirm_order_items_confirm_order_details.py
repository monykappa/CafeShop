# Generated by Django 4.2.2 on 2023-09-14 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0063_remove_orderitem_confirm_confirm_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirm',
            name='order_items',
        ),
        migrations.AddField(
            model_name='confirm',
            name='order_details',
            field=models.ManyToManyField(to='menu.orderdetail'),
        ),
    ]
