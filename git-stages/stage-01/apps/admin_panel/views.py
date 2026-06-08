from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Category, Product
from orders.models import Order
from users.models import User


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'admin' and not request.user.is_superuser:
            messages.error(request, 'Доступ только для администратора')
            return redirect('catalog:index')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html', {
        'users_count': User.objects.count(),
        'products_count': Product.objects.count(),
        'orders_count': Order.objects.count(),
        'orders_new': Order.objects.filter(status='new').count(),
        'low_stock': Product.objects.filter(stock__lte=5, is_active=True),
    })


@login_required
@admin_required
def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'admin_panel/product_list.html', {'products': products})


@login_required
@admin_required
def product_edit(request, product_id=None):
    product = get_object_or_404(Product, id=product_id) if product_id else None
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'

        if product:
            product.name = name
            product.category_id = category_id
            product.price = price
            product.stock = stock
            product.description = description
            product.is_active = is_active
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            product.save()
            messages.success(request, 'Товар обновлён')
        else:
            Product.objects.create(
                name=name,
                category_id=category_id,
                price=price,
                stock=stock,
                description=description,
                is_active=is_active,
                image=request.FILES.get('image'),
            )
            messages.success(request, 'Товар добавлен')
        return redirect('admin_panel:product_list')

    return render(request, 'admin_panel/product_form.html', {
        'product': product,
        'categories': categories,
    })


@login_required
@admin_required
def order_list(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'admin_panel/order_list.html', {
        'orders': orders,
        'selected_status': status,
    })
