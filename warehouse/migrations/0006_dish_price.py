# Generated by Django 4.2.5 on 2023-12-20 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0005_dish_returnable'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
