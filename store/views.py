from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def products_view(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Fetch product by ID
    return render(request, 'store/product_detail.html', {'product': product})

def cart_view(request):
    cart_items = []  # Replace with real cart items from session or database
    total_price = sum(item.product.price * item.quantity for item in cart_items) if cart_items else 0
    total_items = sum(item.quantity for item in cart_items) if cart_items else 0

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    })

def login_view(request):
    return render(request, 'store/login.html')