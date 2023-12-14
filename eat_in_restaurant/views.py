# eat_in_app/views.py
from django.shortcuts import render, redirect
from .models import MenuItem
from .forms import TableForm, OrderForm

def choose_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            selected_table = form.cleaned_data['table']
            request.session['selected_table'] = selected_table
            return redirect('eat_in_restaurant:choose_food_items')
    else:
        form = TableForm()

    return render(request, 'eat_in_restaurant/choose_table.html', {'form': form})


def choose_food_items(request):
    selected_table = request.session.get('selected_table')
    if not selected_table:
        return redirect('eat_in_restaurant:choose_table')

    food_items = MenuItem.objects.filter(category__name=selected_table)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Process the order
            # ...
            return redirect('eat_in_restaurant:choose_table')
    else:
        order_form = OrderForm()

    return render(request, 'eat_in_restaurant/choose_food_items.html', {'food_items': food_items, 'order_form': order_form})