# Generated by Django 4.2.2 on 2023-09-12 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0018_remove_customer_location_customer_district_and_more'),
        ('menu', '0028_remove_checkout_contact_remove_checkout_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.customer'),
        ),
    ]