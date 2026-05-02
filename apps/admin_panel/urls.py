from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryManageView,
    CategoryUpdateView,
    ProductCreateView,
    ProductDeleteView,
    ProductManageListView,
    ProductUpdateView,
    UserManageView,
    UserUpdateView,
)

app_name = "admin_panel"

urlpatterns = [
    path("products/", ProductManageListView.as_view(), name="products"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("categories/", CategoryManageView.as_view(), name="categories"),
    path("categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path("users/", UserManageView.as_view(), name="users"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
]
