from django.conf import settings
from django.db import models

from apps.orders.models import Order, OrderStatus


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    old_status = models.ForeignKey(OrderStatus, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    new_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, related_name="+")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
