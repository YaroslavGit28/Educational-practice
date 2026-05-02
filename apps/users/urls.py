from django.urls import path

from .views import (
    ProfileUpdateView,
    UserLoginView,
    UserLogoutView,
    UserPasswordResetView,
    UserRegisterStepView,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterStepView.as_view(), name="register"),
    path("register/<int:step>/", UserRegisterStepView.as_view(), name="register-step"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("password-reset/", UserPasswordResetView.as_view(), name="password_reset"),
]
