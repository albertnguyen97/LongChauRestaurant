# Generated by Django 4.2.5 on 2023-12-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0006_dish_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, upload_to='dishes/%Y/%m/%d'),
        ),
    ]
