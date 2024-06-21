from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from order_cart.models import OrderCart

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderCart, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        for item in order.items.all():
            # Check if the price is a float and has a decimal part
            if isinstance(item.price, float):
                price = round(item.price)
            else:
                price = int(item.price)

            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': price,
                        'currency': 'vnd',
                        'product_data': {
                            'name': item.dish.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
