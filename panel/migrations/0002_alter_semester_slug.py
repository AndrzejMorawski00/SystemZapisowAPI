# Generated by Django 5.0.7 on 2024-07-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='slug',
            field=models.SlugField(default='1194dfbd-73f4-4861-9205-703c8ad59556', max_length=100),
        ),
    ]
