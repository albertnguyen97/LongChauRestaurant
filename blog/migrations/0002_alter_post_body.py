# Generated by Django 5.0.1 on 2024-05-23 18:37

import django_summernote.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
