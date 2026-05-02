from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

from apps.orders.models import Order, OrderStatus

from .models import OrderStatusHistory


class RoleMixin(LoginRequiredMixin, UserPassesTestMixin):
    roles = []

    def test_func(self):
        return self.request.user.role in self.roles or self.request.user.is_superuser


class ManagerOrdersView(RoleMixin, ListView):
    roles = ["manager", "admin"]
    model = Order
    template_name = "processing/manager_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        qs = Order.objects.select_related("user", "status").order_by("-created_at")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status__name=status)
        return qs


class WarehouseOrdersView(RoleMixin, ListView):
    roles = ["warehouse", "admin"]
    model = Order
    template_name = "processing/warehouse_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(status__name__in=["confirmed", "assembling"]).select_related("user", "status")


class ChangeOrderStatusView(RoleMixin, View):
    roles = ["manager", "warehouse", "admin"]

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        status_name = request.POST.get("status")
        new_status = get_object_or_404(OrderStatus, name=status_name)
        old_status = order.status
        order.status = new_status
        order.save(update_fields=["status"])
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user,
            comment=request.POST.get("comment", ""),
        )
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": True, "order_id": order.id, "status": new_status.name})
        messages.success(request, "Статус обновлен.")
        return redirect(request.META.get("HTTP_REFERER", "processing:manager_orders"))
