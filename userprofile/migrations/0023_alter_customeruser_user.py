# Generated by Django 4.2.2 on 2023-09-15 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0022_alter_customeruser_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_user', to=settings.AUTH_USER_MODEL),
        ),
    ]