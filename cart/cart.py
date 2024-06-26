from decimal import Decimal
from django.conf import settings
from warehouse.models import Dish


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, dish, quantity=1, override_quantity=False):
        dish_id = str(dish.id)
        price = str(dish.discounted_price if dish.discounted_price else dish.price)

        if dish_id not in self.cart:
            self.cart[dish_id] = {'quantity': 0, 'price': price}

        if override_quantity:
            self.cart[dish_id]['quantity'] = quantity
        else:
            self.cart[dish_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, dish):
        dish_id = str(dish.id)
        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def __iter__(self):
        dish_ids = self.cart.keys()
        dishes = Dish.objects.filter(id__in=dish_ids)
        cart = self.cart.copy()
        for dish in dishes:
            cart[str(dish.id)]['dish'] = dish
        for item in cart.values():
            dish = item['dish']
            price = dish.discounted_price if dish.discounted_price else dish.price
            item['price'] = Decimal(price)
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal(0)
        for item in self:
            dish = item['dish']
            price = dish.discounted_price if dish.discounted_price else item['price']
            total += Decimal(price) * item['quantity']
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
