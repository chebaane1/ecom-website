from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.product_list, name='product_list'),
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
]
