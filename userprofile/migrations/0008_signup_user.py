# Generated by Django 4.2.2 on 2023-08-21 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0007_remove_signup_contact_remove_signup_dob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]