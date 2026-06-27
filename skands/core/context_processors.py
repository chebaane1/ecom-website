from .cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {
        'cart_count': cart.get_total_quantity(),
        'cart_total': cart.get_total_price(),
    }
