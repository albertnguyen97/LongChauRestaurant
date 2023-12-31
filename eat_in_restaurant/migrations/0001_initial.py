# Generated by Django 5.0 on 2023-12-14 01:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.category')),
                ('food_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.fooditem')),
            ],
        ),
    ]
