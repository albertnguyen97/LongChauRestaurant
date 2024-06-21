from django.shortcuts import render, redirect, get_object_or_404
from warehouse.models import Dish, Category
from .forms import TableForm, OrderForm
from decimal import Decimal
from django.shortcuts import render, redirect
from warehouse.models import Dish, Category
from .models import Table, Queue, Order
from .forms import TableForm, OrderForm
from decimal import Decimal
from django.contrib import messages  # Import messages module
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet


@login_required
def choose_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            selected_table_id = form.cleaned_data['selected_table']

            # Get the selected table object
            selected_table = Table.objects.get(table_id=selected_table_id)

            # Update the booked status to True
            selected_table.booked = True
            selected_table.save()

            # Store the selected table in session
            request.session['selected_table'] = selected_table_id

            # Redirect to the next page (choose_food_items)
            return redirect('eat_in_restaurant:choose_food_items')
    else:
        form = TableForm()
    tables = Table.objects.all()
    return render(request, 'eat_in_restaurant/choose_table.html', {'form': form, 'tables': tables})

@login_required
def choose_food_items(request):
    selected_table = request.session.get('selected_table')
    if not selected_table:
        return redirect('eat_in_restaurant:choose_table')

    dishes = Dish.objects.all()
    menu_categories = Category.objects.all()

    return render(request, 'eat_in_restaurant/choose_food_items.html', {'food_items': dishes,
                                                                        'menu_categories':  menu_categories,
                                                                        'selected_table': selected_table})

@login_required
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
        for dish, quantity in selected_dishes_quantities.items():
            for _ in range(quantity):
                Queue.objects.create(table_number=Table.objects.get(table_id=selected_table),
                                     dish=dish,
                                     is_cooked=False)  # Set is_cooked to False initially

        messages.success(request, 'Đã gọi món thành công. Vui lòng chờ một chút.')

    return redirect('eat_in_restaurant:choose_food_items')


def calculate_discounted_total(selected_dishes_quantities, discount_percentage):
    # Example function to calculate the discounted total amount based on selected dishes and quantities
    total_price = sum(dish.price * quantity for dish, quantity in selected_dishes_quantities.items())
    discount_amount = (discount_percentage / Decimal('100')) * total_price
    discounted_total = total_price - discount_amount
    return discounted_total


@login_required
def checkout_confirmed(request):
    # Retrieve necessary data from the request or session
    selected_dishes = request.session.get('selected_dishes')
    discounted_total = request.session.get('discounted_total')

    # Retrieve the selected table ID from the session
    selected_table_id = request.session.get('selected_table')

    # Set the booked status of the selected table back to False
    if selected_table_id is not None:
        selected_table = Table.objects.get(table_id=selected_table_id)
        selected_table.booked = False
        selected_table.save()

        # Remove the selected table from the session
        del request.session['selected_table']

    # You can perform additional processing here if needed

    # Render the order_confirmed template with the necessary data
    return render(request, 'eat_in_restaurant/order_confirmation.html', {
        'selected_dishes': selected_dishes,
        'discounted_total': discounted_total,
    })


def save_food_order(request):
    if request.method == 'POST':
        # Retrieve selected dishes from session
        selected_dishes_quantities = request.session.get('selected_dishes_quantities', {})

        request.session.pop('selected_dishes_quantities', None)

        # Redirect to a thank you page or back to the main page
        return redirect('eat_in_restaurant:choose_food_items')


@login_required
def show_finished_dishes(request):
    selected_table_id = request.session.get('selected_table')

    # Ensure there is a selected table
    if not selected_table_id:
        return JsonResponse({'finished_dishes': []})

    selected_table = get_object_or_404(Table, table_id=selected_table_id)
    finished_dishes = Queue.objects.filter(table_number=selected_table, is_cooked=True)
    finished_dishes_list = [dish.dish.name for dish in finished_dishes]

    return JsonResponse({'finished_dishes': finished_dishes_list})


@login_required
def checkout_finished_dishes(request):
    selected_table_id = request.session.get('selected_table')

    # Ensure there is a selected table
    if not selected_table_id:
        return redirect('eat_in_restaurant:choose_food_items')

    selected_table = get_object_or_404(Table, table_id=selected_table_id)
    finished_dishes = Queue.objects.filter(table_number=selected_table, is_cooked=True)

    # Calculate total price for finished dishes
    total_price = sum(dish.dish.price for dish in finished_dishes)

    return render(request, 'eat_in_restaurant/checkout_finished_dishes.html', {
        'selected_table': selected_table,
        'finished_dishes': finished_dishes,
        'total_price': total_price,
    })


def mark_table_not_booked(request):
    selected_table_id = request.session.get('selected_table')

    # Ensure there is a selected table
    if not selected_table_id:
        return redirect('eat_in_restaurant:choose_food_items')

    selected_table = get_object_or_404(Table, table_id=selected_table_id)
    selected_table.booked = False
    selected_table.save()

    order, _ = Order.objects.get_or_create(selected_table=selected_table)

    finished_dishes = Queue.objects.filter(table_number=selected_table, is_cooked=True)

    # Check if there are finished dishes
    if finished_dishes:
        for dish in finished_dishes:
            order.finished_dishes.append(dish)
        finished_dishes.delete()

    del request.session['selected_table']

    messages.success(request, 'Table is now available.')

    return redirect('eat_in_restaurant:choose_table')

