from .models import CartItem


def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_cart_queryset(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user).select_related("product")
    return CartItem.objects.filter(session_key=get_session_key(request)).select_related("product")


def merge_session_cart_to_user(user, session_key):
    for item in CartItem.objects.filter(session_key=session_key, user__isnull=True):
        user_item, created = CartItem.objects.get_or_create(user=user, product=item.product, defaults={"quantity": item.quantity})
        if not created:
            user_item.quantity += item.quantity
            user_item.save(update_fields=["quantity"])
        item.delete()
