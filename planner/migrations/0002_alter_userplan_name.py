# Generated by Django 5.0.7 on 2024-07-22 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userplan',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
