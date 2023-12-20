from django.shortcuts import render, redirect
from warehouse.models import Dish
from .forms import TableForm, OrderForm
from decimal import Decimal


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

    dishes = Dish.objects.all()

    return render(request, 'eat_in_restaurant/choose_food_items.html', {'food_items': dishes,
                                                                        'selected_table': selected_table})


def order_check(request):
    if request.method == 'POST':
        selected_table = request.session.get('selected_table')
        # Check if any dishes are selected
        selected_dishes_quantities = {}
        for dish in Dish.objects.all():
            quantity_key = f'quantity_{dish.id}'
            quantity = int(request.POST.get(quantity_key, 0))
            if quantity > 0:
                selected_dishes_quantities[dish] = quantity

        if not selected_dishes_quantities:
            # No dishes selected, redirect back to choose_food_items
            return redirect('eat_in_restaurant:choose_food_items')

        # Example logic for determining which dishes can be returned
        returned_dishes = []  # List to store dishes that can be returned
        for dish, quantity in selected_dishes_quantities.items():
            # Replace the condition with your actual logic for returning dishes
            if dish.returnable:
                returned_dishes.extend([dish] * quantity)

            # Example logic for applying a discount
            # Replace this with your actual logic for applying discounts
        discount_percentage = Decimal('10')  # Assuming a 10% discount
        discounted_total = calculate_discounted_total(selected_dishes_quantities, discount_percentage)

        # Handling deletion of returned dishes
        # Example logic for applying a discount
        # Replace this with your actual logic for applying discounts

        # Render the order_check template with the necessary data
        return render(request, 'eat_in_restaurant/order_check.html', {
            'selected_table': selected_table,
            'selected_dishes_quantities': selected_dishes_quantities,
            'returned_dishes': returned_dishes,
            'discount_percentage': discount_percentage,
            'discounted_total': discounted_total,
        })

    return redirect('eat_in_restaurant:choose_food_items')


def calculate_discounted_total(selected_dishes_quantities, discount_percentage):
    # Example function to calculate the discounted total amount based on selected dishes and quantities
    total_price = sum(dish.price * quantity for dish, quantity in selected_dishes_quantities.items())
    discount_amount = (discount_percentage / Decimal('100')) * total_price
    discounted_total = total_price - discount_amount
    return discounted_total


def order_confirmed(request):
    # Retrieve necessary data from the request or session
    selected_dishes = request.session.get('selected_dishes')
    discounted_total = request.session.get('discounted_total')

    # You can perform additional processing here if needed

    # Render the order_confirmed template with the necessary data
    return render(request, 'eat_in_restaurant/order_confirmation.html', {
        'selected_dishes': selected_dishes,
        'discounted_total': discounted_total,
    })
