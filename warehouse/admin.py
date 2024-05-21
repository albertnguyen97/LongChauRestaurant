from django.contrib import admin
from .models import Ingredient, Dish, Distributor, Category, Discount
# Register your models here.
admin.site.register(Distributor)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Discount)
