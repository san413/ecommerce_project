from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def products_view(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

def cart_view(request):
    return render(request, 'store/cart.html')

def login_view(request):
    return render(request, 'store/login.html')