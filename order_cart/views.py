from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         dish=item['dish'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            return render(request,
                          'order_cart/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    cart.clear()
    return render(request,
                  'order_cart/order/create.html',
                  {'cart': cart, 'form': form})