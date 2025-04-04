from django.urls import path
from . import views
from .views import products_view, product_detail_view

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_view, name='products'),
    path('products/<int:product_id>/', product_detail_view, name='product_detail'),  # 🔥 Add this!
    path('cart/', views.cart_view, name='cart'),
    path('login/', views.login_view, name='login'),
]
