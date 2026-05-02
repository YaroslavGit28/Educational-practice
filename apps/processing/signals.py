from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.orders.models import Order

from .models import OrderStatusHistory


@receiver(pre_save, sender=Order)
def track_order_status(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = sender.objects.filter(pk=instance.pk).first()
    if old and old.status_id != instance.status_id:
        OrderStatusHistory.objects.create(order=instance, old_status=old.status, new_status=instance.status)
