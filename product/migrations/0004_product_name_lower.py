# Generated by Django 4.1.5 on 2023-08-29 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_productoption_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name_lower',
            field=models.CharField(blank=True, editable=False, max_length=500, null=True),
        ),
    ]
