from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
from io import BytesIO

from apps.catalog.models import Category, Product
from apps.orders.models import OrderStatus
from apps.users.models import User


class Command(BaseCommand):
    help = "Заполнить базу тестовыми данными"

    @staticmethod
    def build_product_image(title):
        image = Image.new("RGB", (600, 400), color=(233, 237, 245))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(30, 30), (570, 370)], outline=(120, 140, 170), width=4)
        draw.text((50, 180), title[:28], fill=(40, 55, 80))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return ContentFile(buffer.getvalue(), name=f"{title.lower().replace(' ', '_')}.png")

    def handle(self, *args, **options):
        roles = [
            ("admin@example.com", "admin"),
            ("manager@example.com", "manager"),
            ("warehouse@example.com", "warehouse"),
            ("buyer1@example.com", "customer"),
            ("buyer2@example.com", "customer"),
        ]
        for email, role in roles:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"full_name": email.split("@")[0], "role": role, "phone": "+70000000000", "is_staff": role == "admin"},
            )
            user.set_password("TestPass123!")
            if role == "admin":
                user.is_staff = True
                user.is_superuser = True
            user.save(update_fields=["password", "is_staff", "is_superuser"])
        cat_names = ["Ручки", "Тетради", "Папки", "Карандаши", "Бумага"]
        categories = [Category.objects.get_or_create(name=name, slug=name.lower())[0] for name in cat_names]
        products_data = [
            ("Ручка гелевая синяя", "Мягкое письмо, 0.5 мм", 129, 45, categories[0]),
            ("Набор ручек 5 цветов", "Для учебы и конспектов", 349, 25, categories[0]),
            ("Тетрадь 48 листов клетка", "Плотная бумага 65 г/м2", 89, 80, categories[1]),
            ("Тетрадь 96 листов линия", "Твердая обложка", 159, 50, categories[1]),
            ("Папка-регистратор A4", "Ширина корешка 70 мм", 299, 35, categories[2]),
            ("Папка на кнопке A4", "Полупрозрачный пластик", 99, 60, categories[2]),
            ("Карандаш HB", "Шестигранный корпус", 39, 120, categories[3]),
            ("Набор цветных карандашей 12 шт", "Яркие насыщенные цвета", 249, 40, categories[3]),
            ("Бумага офисная A4 500л", "Класс C, белизна 146%", 499, 30, categories[4]),
            ("Бумага цветная A4 100л", "Ассорти 5 цветов", 219, 35, categories[4]),
            ("Маркер текстовыделитель", "Скошенный наконечник", 119, 70, categories[0]),
            ("Скотч канцелярский 19мм", "Прозрачный, 33 м", 79, 90, categories[2]),
            ("Стикеры 76x76", "Блок 400 листов", 189, 55, categories[4]),
            ("Ластик мягкий белый", "Не повреждает бумагу", 49, 110, categories[3]),
            ("Линейка 30 см", "Прозрачный пластик", 69, 95, categories[3]),
        ]
        for name, description, price, stock, category in products_data:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "price": price,
                    "stock": stock,
                    "description": description,
                    "is_active": True,
                },
            )
            if created or not product.image:
                product.image.save(
                    f"{name.lower().replace(' ', '_')}.png",
                    self.build_product_image(name),
                    save=True,
                )
        for name in ["new", "confirmed", "assembling", "shipped", "cancelled"]:
            OrderStatus.objects.get_or_create(name=name, defaults={"description": name})
        self.stdout.write(self.style.SUCCESS("Тестовые данные созданы."))
