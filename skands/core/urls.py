from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('v2/', views.home_v2, name='home_v2'),
    path('products/', views.product_list, name='product_list'),
    path('products/v2/', views.product_list_v2, name='product_list_v2'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<uuid:uuid>/', views.order_success, name='order_success'),

    # manager
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/order/<int:pk>/update/', views.order_update, name='order_update'),
    path('manager/summary/', views.sales_summary, name='sales_summary'),
    
    # manager products
    path('manager/products/', views.product_manage_list, name='product_manage_list'),
    path('manager/products/add/', views.product_create, name='product_create'),
    path('manager/products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('manager/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('manager/products/image/<int:image_id>/delete/', views.product_image_delete, name='product_image_delete'),
]

