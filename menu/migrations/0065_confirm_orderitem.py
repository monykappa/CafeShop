# Generated by Django 4.2.2 on 2023-09-14 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0064_remove_confirm_order_items_confirm_order_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirm',
            name='orderItem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.orderitem'),
        ),
    ]
