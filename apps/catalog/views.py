from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product


def index(request):
    products = Product.objects.filter(is_active=True)[:12]
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'catalog/index.html', {
        'products': products,
        'categories': categories,
    })


def catalog(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Фильтрация
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    min_price = request.GET.get('min_price')
    if min_price:
        products = products.filter(price__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(price__lte=max_price)

    in_stock = request.GET.get('in_stock')
    if in_stock:
        products = products.filter(stock__gt=0)

    # Поиск
    q = request.GET.get('q')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    return render(request, 'catalog/catalog.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})