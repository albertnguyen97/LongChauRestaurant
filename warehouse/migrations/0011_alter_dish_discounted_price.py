# Generated by Django 5.0.1 on 2024-04-09 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0010_alter_dish_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
    ]
