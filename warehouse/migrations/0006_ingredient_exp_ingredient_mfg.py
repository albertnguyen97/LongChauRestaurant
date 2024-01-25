# Generated by Django 5.0.1 on 2024-01-25 13:24

import warehouse.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0005_remove_ingredient_exp_remove_ingredient_mfg'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='exp',
            field=models.DateField(blank=True, default='2025-04-04', null=True, validators=[warehouse.models.validate_exp_greater_than_mfg]),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='mfg',
            field=models.DateField(blank=True, default='2023-04-04', null=True),
        ),
    ]