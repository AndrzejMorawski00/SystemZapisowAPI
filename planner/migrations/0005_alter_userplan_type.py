# Generated by Django 5.0.7 on 2024-08-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_userplan_slug_alter_userplan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userplan',
            name='type',
            field=models.CharField(choices=[('Inżynierskie', 'Eng'), ('Licencjackie', 'Bac')], default='', max_length=20),
        ),
    ]
