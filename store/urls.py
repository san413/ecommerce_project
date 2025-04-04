from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_view, name='products'),
    path('cart/', views.cart_view, name='cart'),
    path('login/', views.login_view, name='login'),
]
