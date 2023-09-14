# Generated by Django 4.2.2 on 2023-09-14 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0070_remove_confirm_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirm',
            name='quantity',
        ),
        migrations.CreateModel(
            name='ProductQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('confirm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.confirm')),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.productsize')),
            ],
        ),
        migrations.AlterField(
            model_name='confirm',
            name='products',
            field=models.ManyToManyField(through='menu.ProductQuantity', to='menu.productsize'),
        ),
    ]
