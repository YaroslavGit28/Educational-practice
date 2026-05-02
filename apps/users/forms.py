from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "phone", "address", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "phone", "address")


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class RegisterStep1Form(forms.Form):
    email = forms.EmailField(label="Email")


class RegisterStep2Form(forms.Form):
    full_name = forms.CharField(max_length=255, label="ФИО")


class RegisterStep3Form(forms.Form):
    phone = forms.CharField(max_length=30, label="Телефон")
    address = forms.CharField(widget=forms.Textarea, label="Адрес")


class RegisterStep4Form(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повтор пароля")

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен быть не менее 8 символов.")
        if not any(ch.isdigit() for ch in password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(ch.isupper() for ch in password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data
