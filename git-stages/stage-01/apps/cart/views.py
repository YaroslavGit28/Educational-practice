from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from catalog.models import Product
from .models import CartItem


def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.get_total() for item in cart_items)
    return cart_items, total


def cart_view(request):
    cart_items, total = get_cart(request)
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


def add_to_cart(request, product_id):
    if request.method == 'POST':
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_count = CartItem.objects.filter(session_key=session_key).count()
            return JsonResponse({'success': True, 'cart_count': cart_count})

        return redirect('cart:cart_view')


def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart:cart_view')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:cart_view')