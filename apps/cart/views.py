from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.catalog.models import Product

from .models import CartItem
from .services import get_cart_queryset, get_session_key


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _cart_count(request):
    return sum(i.quantity for i in get_cart_queryset(request))


class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = get_cart_queryset(self.request)
        return context


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        quantity = int(request.POST.get("quantity", 1))
        key = get_session_key(request)
        next_url = request.POST.get("next") or request.GET.get("next")
        defaults = {"quantity": quantity}
        if request.user.is_authenticated:
            item, created = CartItem.objects.get_or_create(user=request.user, product=product, defaults=defaults)
        else:
            item, created = CartItem.objects.get_or_create(session_key=key, product=product, user=None, defaults=defaults)
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
        messages.success(request, "Товар добавлен в корзину.")
        return redirect(next_url or "cart:view")


class UpdateCartItemView(View):
    def post(self, request, item_id):
        queryset = get_cart_queryset(request)
        item = get_object_or_404(queryset, pk=item_id)
        action = request.POST.get("action")
        if action == "inc":
            item.quantity += 1
        elif action == "dec":
            item.quantity = max(1, item.quantity - 1)
        else:
            item.quantity = max(1, int(request.POST.get("quantity", 1)))
        item.save(update_fields=["quantity"])
        return JsonResponse(
            {
                "ok": True,
                "item_id": item.id,
                "qty": item.quantity,
                "line_total": float(item.total_price),
                "cart_count": _cart_count(request),
            }
        )


class RemoveCartItemView(View):
    def post(self, request, item_id):
        queryset = get_cart_queryset(request)
        item = get_object_or_404(queryset, pk=item_id)
        item.delete()
        if _is_ajax(request):
            return JsonResponse({"ok": True, "item_id": item_id, "cart_count": _cart_count(request)})
        messages.warning(request, "Товар удалён из корзины.")
        return redirect("cart:view")


class ClearCartView(View):
    def post(self, request):
        get_cart_queryset(request).delete()
        messages.info(request, "Корзина очищена.")
        return redirect("cart:view")
