# from django.http import HttpResponse
import json
from datetime import datetime
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu, Booking
from .forms import BookingForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from warehouse.models import Dish, Category
from cart.forms import CartAddDishForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .recommender import Recommender

# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def event(request):
    return render(request, 'event.html')


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        reservations_count = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).count()
        if reservations_count < 10:
            booking = Booking(
                first_name=data['first_name'],
                last_name=data['last_name'],
                guest_number=data['guest_number'],
                comment=data['comment'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot']
            )
            booking.save()
        else:
            return HttpResponse('{"error": 1}', content_type='application/json')
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all().filter(reservation_date=date)

    # Serialize the reservation queryset in JSON format
    booking_json = serializers.serialize('json', bookings)

    # Return rendering of HTML template with reservation data in context
    return HttpResponse(booking_json, content_type='application/json')


def show_json(request):
    bookings = Booking.objects.all()

    # Serialize the reservation queryset in JSON format
    booking_data = list(bookings.values())

    # Pass the JSON data to the template
    context = {
        'booking_data': booking_data,
    }

    # Render the template with the JSON data
    return render(request, 'reservations.html', context)


# Add your code here to create new views


def menu(request):
    menu_data = Dish.objects.all()
    categories = Category.objects.all()
    # Pagination
    paginator = Paginator(menu_data, 20)  # Show 10 items per page

    page_number = request.GET.get('page')
    try:
        menu_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        menu_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        menu_data = paginator.page(paginator.num_pages)
    for item in menu_data:
        if item.discounts_dish.exists():
            # Get the highest discount percentage for the item
            max_discount_percent = item.discounts_dish.order_by('-discount_percent').first().discount_percent
            # Calculate discounted price
            discounted_price = item.price - (item.price * (max_discount_percent / 100))
            # Assign the discounted price to the item object
            item.discounted_price = discounted_price
        else:
            # If no discount exists, use the original price as the discounted price
            item.discounted_price = item.price

    main_data = {"menu": menu_data, "categories": categories}
    return render(request, 'menu.html', main_data)


def display_menu_item(request, id):
    dish = get_object_or_404(Dish, id=id, is_available=True)
    cart_dish_form = CartAddDishForm()
    r = Recommender()
    recommended_dishes = r.suggest_dishes_for([dish], 4)
    return render(request, 'menu_item.html', {'dish': dish, 'cart_dish_form': cart_dish_form,
                                              'recommended_dishes': recommended_dishes
                                              })
