from django.shortcuts import render, get_object_or_404
from .models import Dish, Ingredient


def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'cuisine/dish_list.html', {'dishes': dishes})


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, 'cuisine/dish_detail.html', {'dish': dish})


def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'cuisine/ingredient_list.html', {'ingredients': ingredients})


def ingredient_detail(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return render(request, 'cuisine/ingredient_detail.html', {'ingredient': ingredient})
