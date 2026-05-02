from django.urls import path

from .views import HomeView, ProductDetailView, ProductListView

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("catalog/", ProductListView.as_view(), name="product_list"),
    path("catalog/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
