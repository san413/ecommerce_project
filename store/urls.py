from django.urls import path, include  # ✅ Add include here
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_view, name='products'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),  # Comma added here ✅
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login_view, name='login'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-history/', views.order_history, name='order_history'),

    
    path('dashboard/', include('dashboard.urls')),  # 👈 Add this line


]
