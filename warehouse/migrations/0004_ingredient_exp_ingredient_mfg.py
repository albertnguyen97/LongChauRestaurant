# Generated by Django 5.0.1 on 2024-01-25 12:59

import warehouse.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_dish_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='exp',
            field=models.DateField(blank=True, default='2025-02-02', validators=[warehouse.models.validate_exp_greater_than_mfg]),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='mfg',
            field=models.DateField(blank=True, default='2022-02-02'),
        ),
    ]