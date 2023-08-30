# Generated by Django 4.1.5 on 2023-08-29 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='carousel_images/')),
                ('link', models.CharField(default='/', max_length=500)),
            ],
        ),
    ]
