from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.views.generic import DetailView, FormView, ListView

from apps.cart.services import get_cart_queryset

from .forms import CheckoutForm
from .models import Order, OrderItem, OrderStatus


class CheckoutView(FormView):
    template_name = "orders/checkout.html"
    form_class = CheckoutForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        cart_items = get_cart_queryset(self.request)
        if not cart_items.exists():
            messages.error(self.request, "Корзина пуста.")
            return redirect("cart:view")
        with transaction.atomic():
            status = OrderStatus.objects.get_or_create(name="new", defaults={"description": "Новый заказ"})[0]
            order = form.save(commit=False)
            if self.request.user.is_authenticated:
                order.user = self.request.user
                order.full_name = self.request.user.full_name
                order.phone = self.request.user.phone
                order.delivery_address = self.request.user.address
            else:
                order.user = None
            order.status = status
            order.total_amount = 0
            order.save()
            total = 0
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_moment=item.product.price,
                )
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save(update_fields=["stock"])
                total += item.product.price * item.quantity
            order.total_amount = total
            order.save(update_fields=["total_amount"])
            cart_items.delete()
        messages.success(self.request, "Заказ успешно оформлен.")
        if self.request.user.is_authenticated:
            return redirect("orders:detail", pk=order.pk)
        return redirect("catalog:home")


class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("status").order_by("-created_at")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        if self.request.user.role in {"manager", "warehouse", "admin"} or self.request.user.is_superuser:
            return Order.objects.all().prefetch_related("items__product", "status")
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product", "status")


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        if order.status.name in {"shipped", "cancelled"}:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": False, "detail": "cannot_cancel"}, status=400)
            messages.error(request, "Этот заказ нельзя отменить.")
            return redirect("orders:my_orders")
        cancelled_status, _ = OrderStatus.objects.get_or_create(
            name="cancelled",
            defaults={"description": "Заказ отменён пользователем"},
        )
        order.status = cancelled_status
        order.save(update_fields=["status"])
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "order_id": order.id, "status": cancelled_status.name})
        messages.warning(request, f"Заказ #{order.id} отменён.")
        return redirect("orders:my_orders")
