from django.conf import settings
from django.db import models

from apps.catalog.models import Product


class CartItem(models.Model):
    session_key = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session_key", "user", "product")

    @property
    def total_price(self):
        return self.product.price * self.quantity
