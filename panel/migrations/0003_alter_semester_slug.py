# Generated by Django 5.0.7 on 2024-07-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_alter_semester_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
