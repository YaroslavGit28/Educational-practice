from django.db import OperationalError, ProgrammingError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'customer'
            user.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('catalog:index')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        try:
            user = authenticate(request, email=email, password=password)
        except (OperationalError, ProgrammingError):
            messages.error(
                request,
                'База данных не готова. Выполните: python manage.py migrate && python manage.py load_demo_data',
            )
            return render(request, 'users/login.html')

        if user is not None:
            backend = getattr(user, 'backend', 'users.backends.EmailBackend')
            login(request, user, backend=backend)
            next_url = request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('catalog:index')
        messages.error(request, 'Неверный email или пароль')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('catalog:index')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})