from django.db import models
from users.models import User
from catalog.models import Product


class OrderStatus(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('assembling', 'Собирается'),
        ('shipped', 'Отгружен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    delivery_address = models.TextField('Адрес доставки')
    phone = models.CharField('Телефон', max_length=20)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField('Цена на момент заказа', max_digits=10, decimal_places=2)

    def get_total(self):
        return self.price * self.quantity