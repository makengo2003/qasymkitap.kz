# Generated by Django 4.1.5 on 2023-08-29 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productoption_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoption',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='product.product'),
        ),
    ]
