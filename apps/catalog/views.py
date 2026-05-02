from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Category, Product


class HomeView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by("-created_at")[:8]


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category")
        query = self.request.GET.get("q")
        category_slug = self.request.GET.get("category")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        in_stock = self.request.GET.get("in_stock")

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                child_ids = list(category.children.values_list("id", flat=True))
                queryset = queryset.filter(category_id__in=[category.id, *child_ids])
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if in_stock:
            queryset = queryset.filter(stock__gt=0)
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
