from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/pending/', views.pending_order_list, name='pending_orders'),
    path('orders/paid/', views.paid_order_list, name='paid_orders'),
]
