from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.catalog.models import Category, Product
from apps.users.models import User

from .forms import CategoryForm, ProductForm, UserAdminForm


class AdminRoleMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "admin" or self.request.user.is_superuser


class ProductManageListView(AdminRoleMixin, ListView):
    model = Product
    template_name = "admin_panel/products.html"
    context_object_name = "products"


class ProductCreateView(AdminRoleMixin, CreateView):
    form_class = ProductForm
    template_name = "admin_panel/form.html"
    success_url = reverse_lazy("admin_panel:products")


class ProductUpdateView(AdminRoleMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "admin_panel/form.html"
    success_url = reverse_lazy("admin_panel:products")


class ProductDeleteView(AdminRoleMixin, DeleteView):
    model = Product
    template_name = "admin_panel/confirm_delete.html"
    success_url = reverse_lazy("admin_panel:products")


class CategoryManageView(AdminRoleMixin, ListView):
    model = Category
    template_name = "admin_panel/categories.html"
    context_object_name = "categories"


class CategoryCreateView(AdminRoleMixin, CreateView):
    form_class = CategoryForm
    template_name = "admin_panel/form.html"
    success_url = reverse_lazy("admin_panel:categories")


class CategoryUpdateView(AdminRoleMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "admin_panel/form.html"
    success_url = reverse_lazy("admin_panel:categories")


class UserManageView(AdminRoleMixin, ListView):
    model = User
    template_name = "admin_panel/users.html"
    context_object_name = "users"


class UserUpdateView(AdminRoleMixin, UpdateView):
    model = User
    form_class = UserAdminForm
    template_name = "admin_panel/form.html"
    success_url = reverse_lazy("admin_panel:users")
