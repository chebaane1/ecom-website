from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Product


class Cart:
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)
        if not cart:
            cart = self.session[self.SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, size='', color=''):
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        pid = str(product_id)
        price_str = str(product.price)
        item = self.cart.get(pid)
        if item:
            item['quantity'] = int(item['quantity']) + int(quantity)
            # update size/color to last chosen (UI responsibility to manage)
            item['selected_size'] = size
            item['selected_color'] = color
        else:
            self.cart[pid] = {
                'quantity': int(quantity),
                'price': price_str,
                'selected_size': size,
                'selected_color': color,
            }
        self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def update(self, product_id, quantity):
        pid = str(product_id)
        if pid not in self.cart:
            return
        quantity = int(quantity)
        if quantity <= 0:
            self.remove(product_id)
        else:
            self.cart[pid]['quantity'] = quantity
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self.cart.values():
            total += Decimal(item['price']) * int(item['quantity'])
        return total

    def get_total_quantity(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def __len__(self):
        return len(self.cart)

    def __bool__(self):
        return bool(self.cart)

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}
        for pid, item in list(self.cart.items()):
            product = product_map.get(pid)
            if not product:
                continue
            item_data = item.copy()
            item_data['product'] = product
            item_data['price'] = Decimal(item_data['price'])
            item_data['total_price'] = item_data['price'] * int(item_data['quantity'])
            yield item_data
