from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text')
    search_fields = ('product__name', 'alt_text')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'selected_size', 'selected_color')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id_unique', 'full_name', 'phone_number', 'city', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'city')
    search_fields = ('full_name', 'phone_number', 'id_unique')
    inlines = (OrderItemInline,)
