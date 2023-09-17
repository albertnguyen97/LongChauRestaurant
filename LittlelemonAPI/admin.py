from django.contrib import admin
from .models import MenuItem, Category, Rating, Cart, OrderItem, Order

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
