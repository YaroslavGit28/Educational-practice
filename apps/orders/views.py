from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.views import get_cart
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart_items, total = get_cart(request)

    if not cart_items:
        messages.warning(request, 'Корзина пуста')
        return redirect('catalog:index')

    if request.method == 'POST':
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(
                    request,
                    f'Недостаточно товара «{item.product.name}» на складе (осталось {item.product.stock})',
                )
                return redirect('cart:cart_view')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            delivery_address=request.POST.get('delivery_address'),
            phone=request.POST.get('phone'),
            comment=request.POST.get('comment', ''),
            status='new'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # Уменьшаем остаток на складе
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Очищаем корзину
        cart_items.delete()

        messages.success(request, f'Заказ #{order.id} успешно оформлен!')
        return redirect('orders:order_history')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})