from .services import get_cart_queryset


def cart_summary(request):
    cart_items = get_cart_queryset(request)
    total_qty = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)
    return {"cart_count": total_qty, "cart_total": total_price}
