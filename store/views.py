from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Cart, Order, OrderItem

# Home page
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# All products
def products_view(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

# Product detail
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# Add to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# Update cart item quantity
@require_POST
def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

# Remove from cart
@require_POST
def remove_from_cart(request, product_id):
    cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart')

# View cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    })

# Checkout
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart')  # Nothing to order

    total = sum(item.product.price * item.quantity for item in cart_items)

    # Create order
    order = Order.objects.create(user=request.user, total_price=total)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    # Clear cart
    cart_items.delete()

    return redirect('order_success')  # You’ll define this next

@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

# Login view
def login_view(request):
    return render(request, 'store/login.html')
