from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum

from .models import Product, Order, OrderItem, ProductImage
from .cart import Cart
from .forms import CheckoutForm, OrderStatusForm, ProductForm


def product_list(request):
    products = Product.objects.filter(is_active=True)
    print(f"DEBUG: Retrieved {products.count()} active products for product list view.")
    return render(request, 'core/product_list.html', {'products': products})


def home(request):
    """Render the homepage with a selection of products."""
    products = Product.objects.filter(is_active=True)[:8]
    featured = products[:4]
    print(f"DEBUG: Retrieved {products.count()} active products for homepage view.")
    categories = [
        {'name': 'Robes', 'icon': 'core/images/svgs/robe.svg'},
        {'name': 'Tops', 'icon': 'core/images/svgs/top.svg'},
        {'name': 'Bas', 'icon': 'core/images/svgs/bas.svg'},
        {'name': 'Sacs', 'icon': 'core/images/svgs/sac.svg'},
        {'name': 'Chaussures', 'icon': 'core/images/svgs/chaussure.svg'},
    ]
    hero_mobile_slides = [
        {'image': 'core/images/hero-mobile/1.jpg', 'alt': 'Nouvelle collection — Robes'},
        {'image': 'core/images/hero-mobile/2.jpg', 'alt': 'Sacs & accessoires tendance'}
    ]
    return render(
        request,
        'core/home.html',
        {
            'products': products,
            'featured': featured,
            'categories': categories,
            'hero_mobile_slides': hero_mobile_slides,
        },
    )


def home_v2(request):
    """Render the V2 homepage with massive category hero banners."""
    products = Product.objects.filter(is_active=True)[:8]
    featured = products[:4]
    print(f"DEBUG: Retrieved {products.count()} active products for homepage V2 view.")
    categories = [
        {
            'name': 'Robes',
            'subtitle': 'Élégance fluide pour toutes vos occasions',
            'image': 'core/images/robes_banner.png',
            'url': '/products/?q=robe'
        },
        {
            'name': 'Tops',
            'subtitle': 'Des hauts modernes et essentiels du quotidien',
            'image': 'core/images/tops_banner.png',
            'url': '/products/?q=top'
        },
        {
            'name': 'Bas',
            'subtitle': 'Coupes parfaites et matières nobles',
            'image': 'core/images/bas_banner.png',
            'url': '/products/?q=bas'
        },
        {
            'name': 'Sacs',
            'subtitle': 'L’accessoire signature de votre garde-robe',
            'image': 'core/images/sacs_banner.png',
            'url': '/products/?q=sac'
        },
        {
            'name': 'Chaussures',
            'subtitle': 'Faites sensation à chaque pas',
            'image': 'core/images/chaussures_banner.png',
            'url': '/products/?q=chaussure'
        },
    ]
    hero_mobile_slides = [
        {'image': 'core/images/hero-mobile/1.jpg', 'alt': 'Nouvelle collection — Robes'},
        {'image': 'core/images/hero-mobile/2.jpg', 'alt': 'Sacs & accessoires tendance'}
    ]
    return render(
        request,
        'core/home_v2.html',
        {
            'products': products,
            'featured': featured,
            'categories': categories,
            'hero_mobile_slides': hero_mobile_slides,
        },
    )


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


def manager_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')[:50]
    return render(request, 'core/manager/dashboard.html', {'orders': orders})


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


def sales_summary(request):
    total = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales'] or Decimal('0.00')
    count = Order.objects.count()
    return render(request, 'core/manager/summary.html', {'total_sales': total, 'order_count': count})


def product_manage_list(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'core/manager/product_manage_list.html', {
        'products': products,
        'query': query
    })


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            uploaded_images = request.FILES.getlist('images')
            for f in uploaded_images:
                ProductImage.objects.create(product=product, image=f)
            messages.success(request, f"Produit '{product.name}' créé avec succès.")
            return redirect(reverse('core:product_manage_list'))
        else:
            print(form.errors)
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ProductForm()
    return render(request, 'core/manager/product_form.html', {
        'form': form,
        'action': 'create'
    })


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            uploaded_images = request.FILES.getlist('images')
            for f in uploaded_images:
                ProductImage.objects.create(product=product, image=f)
            messages.success(request, f"Produit '{product.name}' mis à jour avec succès.")
            return redirect(reverse('core:product_manage_list'))
        else:
            print(form.errors)
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/manager/product_form.html', {
        'form': form,
        'product': product,
        'action': 'update'
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Produit '{name}' supprimé avec succès.")
        return redirect(reverse('core:product_manage_list'))
    return render(request, 'core/manager/product_confirm_delete.html', {'product': product})


def product_image_delete(request, image_id):
    image = get_object_or_404(ProductImage, pk=image_id)
    product_id = image.product.pk
    image.delete()
    messages.success(request, "Image supprimée.")
    return redirect(reverse('core:product_update', args=[product_id]))

