from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Родительская категория')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Остаток', default=0)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Фото', upload_to='products/', null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name