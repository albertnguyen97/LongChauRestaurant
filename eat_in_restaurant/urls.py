from django.urls import path
from .views import choose_table, choose_food_items

app_name = 'eat_in_restaurant'

urlpatterns = [
    path('choose-table/', choose_table, name='choose_table'),
    path('choose-food-items/', choose_food_items, name='choose_food_items'),
]