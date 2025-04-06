from django.shortcuts import render
from store.models import Product, Order

def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(is_paid=False).count()
    paid_orders = Order.objects.filter(is_paid=True).count()

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'paid_orders': paid_orders,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'dashboard/product_list.html', {'products': products})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'dashboard/order_list.html', {'orders': orders})

def pending_order_list(request):
    orders = Order.objects.filter(is_paid=False)
    return render(request, 'dashboard/pending_orders.html', {'orders': orders})

def paid_order_list(request):
    orders = Order.objects.filter(is_paid=True)
    return render(request, 'dashboard/paid_orders.html', {'orders': orders})
