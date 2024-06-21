from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItemCart, OrderCart
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
import weasyprint
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

#
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          dish=item['dish'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             # clear the cart
#             return render(request,
#                           'order_cart/order/created.html',
#                           {'order': order})
#     else:
#         form = OrderCreateForm()
#     cart.clear()
#     return render(request,
#                   'order_cart/order/create.html',
#                   {'cart': cart, 'form': form})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                dish = item['dish']
                quantity = item['quantity']
                # Deduct the quantity of ingredients associated with the dish
                for ingredient in dish.ingredients.all():
                    if ingredient.quantity_product >= quantity:
                        ingredient.quantity_product -= quantity
                        ingredient.save()
                    else:
                        # Handle insufficient quantity scenario (optional)
                        pass
                # Create OrderItem for the ordered dish
                OrderItemCart.objects.create(order=order,
                                         dish=dish,
                                         price=item['price'],
                                         quantity=quantity)
            # Clear the cart
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('payment:process')
            # return render(request, 'order_cart/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order_cart/order/create.html', {'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(OrderCart, id=order_id)
    return render(
        request, 'admin/order_cart/order/detail.html', {'order': order}
    )


def admin_order_pdf(request, order_id):
    order = get_object_or_404(OrderCart, id=order_id)
    html = render_to_string('order_cart/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))]
    )
    return response