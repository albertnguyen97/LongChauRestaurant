# Generated by Django 5.0.1 on 2024-05-22 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_cart', '0001_initial'),
        ('warehouse', '0014_alter_discount_discount_percent'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='OrderCart',
        ),
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='OrderItemCart',
        ),
        migrations.RenameIndex(
            model_name='ordercart',
            new_name='order_cart__created_81e31b_idx',
            old_name='order_cart__created_9cba37_idx',
        ),
    ]