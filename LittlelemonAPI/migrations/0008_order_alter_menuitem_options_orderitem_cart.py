# Generated by Django 4.2.4 on 2023-09-17 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LittlelemonAPI', '0007_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_shipped', models.BooleanField(default=False)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('shipping_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('date', models.DateTimeField(db_index=True)),
                ('delivery_crew', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_as_delivery_crew', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'verbose_name': 'Menu Item', 'verbose_name_plural': 'Menu items'},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('menuitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LittlelemonAPI.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LittlelemonAPI.order')),
            ],
            options={
                'unique_together': {('order', 'menuitem')},
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('menuitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LittlelemonAPI.menuitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('menuitem', 'user')},
            },
        ),
    ]