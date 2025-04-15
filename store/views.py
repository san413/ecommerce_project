from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Cart, Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import razorpay
from django.conf import settings
from store.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

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

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@staff_member_required
def admin_dashboard(request):
    from .models import Product, Order, Cart

    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_pending = Order.objects.filter(is_paid=False).count()
    total_paid = Order.objects.filter(is_paid=True).count()

    return render(request, 'store/admin_dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_pending': total_pending,
        'total_paid': total_paid,
    })

@staff_member_required
def admin_products_list(request):
    products = Product.objects.all()
    return render(request, 'store/admin_products.html', {'products': products})


@staff_member_required
def all_orders(request):
    orders = Order.objects.all()
    return render(request, 'store/admin_orders.html', {'orders': orders})


@staff_member_required
def pending_orders(request):
    orders = Order.objects.filter(is_paid=False)
    return render(request, 'store/admin_orders.html', {'orders': orders})


@staff_member_required
def paid_orders(request):
    orders = Order.objects.filter(is_paid=True)
    return render(request, 'store/admin_orders.html', {'orders': orders})

def make_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # You can replace this with real payment integration
    order.is_paid = True
    order.save()

    return redirect('order_history')  # Replace with your actual URL name

def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        'amount': int(order.total_price * 100),  # Razorpay uses paise
        'currency': 'INR',
        'payment_capture': 1
    })

    order.razorpay_order_id = payment['id']
    order.save()

    context = {
        'order': order,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    }

    return render(request, 'store/payment.html', context)

def payment_success(request):
    return render(request, 'store/payment_success.html')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        params_dict = {
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_order_id': request.POST.get('razorpay_order_id'),
            'razorpay_signature': request.POST.get('razorpay_signature')
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            # Find the matching order using razorpay_order_id
            order = Order.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
            order.is_paid = True
            order.save()

            messages.success(request, f"Payment successful for Order #{order.id}")
            return render(request, 'store/payment_success.html', {'order': order})

        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed.")
            return redirect('home')

    return redirect('home')

def payment_confirmation(request):
    if request.method == 'POST':
        # Do something here like mark order as paid
        # e.g., update order status
        return redirect('order_success')  # or any success page
    return redirect('home')  # fallback

# Login view
def login_view(request):
    return render(request, 'store/login.html')
