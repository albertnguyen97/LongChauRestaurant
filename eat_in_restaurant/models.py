# eat_in_app/models.py
from django.db import models
from warehouse.models import Dish, Category  # Import the FoodItem model


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_item = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name