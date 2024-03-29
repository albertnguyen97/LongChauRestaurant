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
from warehouse.models import Dish
from cart.forms import CartAddDishForm

# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


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


# Add your code here to create new views


def menu(request):
    menu_data = Dish.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)


def display_menu_item(request, id):
    dish = get_object_or_404(Dish, id=id, is_available=True)
    cart_dish_form = CartAddDishForm()
    return render(request, 'menu_item.html', {'dish': dish, 'cart_dish_form': cart_dish_form})

