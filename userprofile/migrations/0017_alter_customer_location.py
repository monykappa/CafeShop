# Generated by Django 4.2.2 on 2023-09-11 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0016_remove_customeruser_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='location',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
