from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from catalog.models import Category, Product
from orders.models import Order, OrderItem


class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.customer = User.objects.create_user(
            email='test_customer@shop.ru',
            password='testpass123',
            full_name='Тестовый Покупатель',
            role='customer',
        )

    def test_health_returns_json(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])

    def test_order_detail_requires_auth(self):
        response = self.client.get('/orders/1/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)

    def test_order_detail_foreign_access_denied(self):
        User = get_user_model()
        other = User.objects.create_user(
            email='other@shop.ru', password='pass', full_name='Другой', role='customer'
        )
        cat = Category.objects.create(name='Тест', slug='test-cat')
        product = Product.objects.create(
            name='Тест', category=cat, price=100, stock=10, is_active=True
        )
        order = Order.objects.create(
            user=other, total_amount=100, delivery_address='Адрес', phone='123', status='new'
        )
        OrderItem.objects.create(order=order, product=product, quantity=1, price=100)

        self.client.force_login(self.customer)
        response = self.client.get(f'/orders/{order.id}/')
        self.assertEqual(response.status_code, 404)
