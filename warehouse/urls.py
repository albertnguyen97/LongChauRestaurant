from django.urls import path
from .views import dish_list, dish_detail, ingredient_list, ingredient_detail

urlpatterns = [
    path('dishes/', dish_list, name='dish_list'),
    path('dishes/<int:dish_id>/', dish_detail, name='dish_detail'),
    path('ingredients/', ingredient_list, name='ingredient_list'),
    path('ingredients/<int:ingredient_id>/', ingredient_detail, name='ingredient_detail'),
]