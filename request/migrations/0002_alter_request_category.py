# Generated by Django 4.1.5 on 2023-08-29 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='category',
            field=models.CharField(choices=[('books', 'BOOKS'), ('languages', 'LANGUAGES'), ('certificates', 'CERTIFICATES')], max_length=50),
        ),
    ]
