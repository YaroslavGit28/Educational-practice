from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import (
    EmailAuthenticationForm,
    ProfileForm,
    RegisterStep1Form,
    RegisterStep2Form,
    RegisterStep3Form,
    RegisterStep4Form,
)
from .models import User


class UserRegisterStepView(FormView):
    template_name = "users/register_step.html"
    success_url = reverse_lazy("users:login")
    session_key = "register_wizard"

    forms_by_step = {
        1: RegisterStep1Form,
        2: RegisterStep2Form,
        3: RegisterStep3Form,
        4: RegisterStep4Form,
    }

    def dispatch(self, request, *args, **kwargs):
        self.step = int(kwargs.get("step", 1))
        if self.step not in self.forms_by_step:
            return redirect("users:register")
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return self.forms_by_step[self.step]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step"] = self.step
        context["total_steps"] = 4
        return context

    def form_valid(self, form):
        wizard_data = self.request.session.get(self.session_key, {})
        wizard_data.update(form.cleaned_data)
        if self.step == 1 and User.objects.filter(email=wizard_data["email"]).exists():
            form.add_error("email", "Пользователь с таким email уже существует.")
            return self.form_invalid(form)
        self.request.session[self.session_key] = wizard_data
        self.request.session.modified = True
        if self.step < 4:
            return redirect("users:register-step", step=self.step + 1)
        user = User(
            email=wizard_data["email"],
            full_name=wizard_data["full_name"],
            phone=wizard_data["phone"],
            address=wizard_data["address"],
            role="customer",
        )
        user.set_password(wizard_data["password1"])
        user.save()
        self.request.session.pop(self.session_key, None)
        messages.success(self.request, "Регистрация завершена. Теперь войдите в аккаунт.")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:home")


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")
    success_message = "Профиль обновлён."

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.txt"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        messages.info(self.request, "Инструкция отправлена на почту.")
        return super().form_valid(form)
