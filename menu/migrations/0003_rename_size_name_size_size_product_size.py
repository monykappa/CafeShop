# Generated by Django 4.2.2 on 2023-09-02 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='size_name',
            new_name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, null=True, to='menu.size'),
        ),
    ]