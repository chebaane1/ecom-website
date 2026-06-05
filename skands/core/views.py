from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum

from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm, OrderStatusForm


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'core/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'core/product_detail.html', {'product': product})


def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', '')
        color = request.POST.get('color', '')
        cart = Cart(request)
        cart.add(product_id=product_id, quantity=quantity, size=size, color=color)
        messages.success(request, 'Produit ajouté au panier.')
    return redirect(request.META.get('HTTP_REFERER', reverse('core:cart_detail')))


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.info(request, 'Article retiré du panier.')
    return redirect(reverse('core:cart_detail'))


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'core/cart_detail.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = cart.get_total_price()
            order.save()
            # create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=int(item['quantity']),
                    price=Decimal(item['price']),
                    selected_size=item.get('selected_size', ''),
                    selected_color=item.get('selected_color', ''),
                )
            cart.clear()
            messages.success(request, 'Commande passée avec succès. Nous vous contacterons pour la livraison.')
            return redirect(reverse('core:order_success', args=[order.id_unique]))
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = CheckoutForm()
    return render(request, 'core/checkout.html', {'cart': cart, 'form': form})


def order_success(request, uuid):
    order = get_object_or_404(Order, id_unique=uuid)
    return render(request, 'core/order_success.html', {'order': order})


@user_passes_test(lambda u: u.is_staff)
def manager_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')[:50]
    return render(request, 'core/manager/dashboard.html', {'orders': orders})


@user_passes_test(lambda u: u.is_staff)
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statut de la commande mis à jour.')
            return redirect(reverse('core:manager_dashboard'))
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'core/manager/order_update.html', {'order': order, 'form': form})


@user_passes_test(lambda u: u.is_staff)
def sales_summary(request):
    total = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales'] or Decimal('0.00')
    count = Order.objects.count()
    return render(request, 'core/manager/summary.html', {'total_sales': total, 'order_count': count})
