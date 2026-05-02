from django import forms

from apps.catalog.models import Category, Product
from apps.users.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "phone", "address", "role", "is_active")
