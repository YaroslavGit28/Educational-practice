from .models import CartItem

def cart_count(request):
    count = 0
    if request.session.session_key:
        count = CartItem.objects.filter(session_key=request.session.session_key).count()
    return {'cart_count': count}