from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'old_price', 'is_active', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('is_active', 'category')


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
