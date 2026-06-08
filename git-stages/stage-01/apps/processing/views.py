from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            if request.user.role not in allowed_roles:
                messages.error(request, 'Нет доступа')
                return redirect('catalog:index')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@login_required
@role_required(['manager', 'admin'])
def manager_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'processing/manager_orders.html', {'orders': orders})

@login_required
@role_required(['manager', 'admin'])
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'confirmed'
    order.save()
    messages.success(request, f'Заказ #{order.id} подтверждён')
    return redirect('processing:manager_orders')

@login_required
@role_required(['manager', 'admin'])
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'cancelled':
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        order.status = 'cancelled'
        order.save()
    messages.warning(request, f'Заказ #{order.id} отменён')
    return redirect('processing:manager_orders')

@login_required
@role_required(['warehouse', 'admin'])
def warehouse_orders(request):
    orders = Order.objects.filter(status='confirmed').order_by('-created_at')
    return render(request, 'processing/warehouse_orders.html', {'orders': orders})

@login_required
@role_required(['warehouse', 'admin'])
def start_pickup(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'assembling'
    order.save()
    messages.success(request, f'Начата сборка заказа #{order.id}')
    return redirect('processing:warehouse_orders')

@login_required
@role_required(['warehouse', 'admin'])
def complete_pickup(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'shipped'
    order.save()
    messages.success(request, f'Заказ #{order.id} собран и отправлен')
    return redirect('processing:warehouse_orders')