# Generated by Django 5.0.1 on 2024-04-02 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_discount_dish_discounts_dish'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='discounted_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]