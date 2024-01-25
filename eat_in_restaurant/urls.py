from django.urls import path
from .views import choose_table, choose_food_items, order_check, checkout_confirmed, save_food_order, show_finished_dishes, checkout_finished_dishes, mark_table_not_booked
app_name = 'eat_in_restaurant'

urlpatterns = [
    path('choose-table/', choose_table, name='choose_table'),
    path('choose-food-items/', choose_food_items, name='choose_food_items'),
    path('save_food_order/', save_food_order, name='save_food_order'),
    path('order_check/', order_check, name='order_check'),
    path('order_confirmed/', checkout_confirmed, name='order_confirmed'),
    path('show_finished_dishes/', show_finished_dishes, name='show_finished_dishes'),
    path('checkout_finished_dishes/', checkout_finished_dishes, name='checkout_finished_dishes'),
    path('mark-table-not-booked/', mark_table_not_booked, name='mark_table_not_booked'),
]
