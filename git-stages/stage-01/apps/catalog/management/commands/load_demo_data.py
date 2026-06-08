from decimal import Decimal

from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from users.models import User


class Command(BaseCommand):
    help = 'Загрузка демонстрационных данных для интернет-магазина'

    def handle(self, *args, **options):
        users_data = [
            ('admin@shop.ru', 'Администратор Системы', 'admin', True, True),
            ('manager@shop.ru', 'Иванов Иван Менеджер', 'manager', False, True),
            ('warehouse@shop.ru', 'Петров Пётр Кладовщик', 'warehouse', False, True),
            ('customer@shop.ru', 'Сидорова Анна Покупатель', 'customer', False, False),
        ]
        for email, name, role, is_super, is_staff in users_data:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    password='demo1234',
                    full_name=name,
                    role=role,
                    phone='+7 (999) 000-00-00',
                )
                user.is_superuser = is_super
                user.is_staff = is_staff
                user.save()
                self.stdout.write(f'Создан пользователь: {email} / demo1234')

        categories_data = [
            ('Ручки и карандаши', 'ruchki-karandashi'),
            ('Бумага и тетради', 'bumaga-tetradi'),
            ('Папки и файлы', 'papki-faily'),
        ]
        categories = {}
        for name, slug in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            categories[slug] = cat

        products_data = [
            ('Ручка шариковая синяя', 'ruchki-karandashi', '45.00', 100, 'Шариковая ручка с синими чернилами'),
            ('Карандаш HB', 'ruchki-karandashi', '25.00', 150, 'Графитовый карандаш твёрдости HB'),
            ('Тетрадь 48 листов', 'bumaga-tetradi', '65.00', 80, 'Тетрадь в линейку, 48 листов'),
            ('Блокнот А5', 'bumaga-tetradi', '120.00', 50, 'Блокнот формата А5, 96 листов'),
            ('Папка-регистратор', 'papki-faily', '250.00', 30, 'Папка-регистратор на 400 листов'),
            ('Скрепки 28 мм (100 шт)', 'papki-faily', '35.00', 200, 'Скрепки металлические 28 мм'),
        ]
        for name, cat_slug, price, stock, desc in products_data:
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': categories[cat_slug],
                    'price': Decimal(price),
                    'stock': stock,
                    'description': desc,
                    'is_active': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Демо-данные успешно загружены'))
