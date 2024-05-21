from django.utils import timezone

from django.db import models
from warehouse.models import Dish, Distributor, Category # Import the FoodItem model


class Table(models.Model):
    table_id = models.IntegerField(primary_key=True)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.table_id}"


class Order(models.Model):
    selected_table = models.CharField(max_length=255)
    finished_dishes = models.JSONField(blank=True, default=list)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_issued = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for Table {self.selected_table}"


class Invoice(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')

    def __str__(self):
        return f"Invoice for Order {self.order_id}"


class Queue(models.Model):
    table_number = models.ForeignKey(Table, on_delete=models.CASCADE, to_field='table_id')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    is_cooked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line to include a creation timestamp
