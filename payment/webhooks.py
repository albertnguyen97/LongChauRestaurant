import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from order_cart.models import OrderCart
from restaurant.recommender import Recommender
from warehouse.models import Dish
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = OrderCart.objects.get(
                    id=session.client_reference_id
                )
            except OrderCart.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            dishes_ids = order.items.values_list('dish_id')
            dishes = Dish.objects.filter(id__in=dishes_ids)
            r = Recommender()
            r.dishes_bought(dishes)
            # payment_completed.delay(order.id)
    return HttpResponse(status=200)

