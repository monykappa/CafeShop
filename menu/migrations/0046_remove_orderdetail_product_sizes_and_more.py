# Generated by Django 4.2.2 on 2023-09-13 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0045_remove_checkout_order_remove_orderdetail_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='product_sizes',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.productsize'),
        ),
    ]