from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("users:login")
            if request.user.role not in roles:
                messages.error(request, "Недостаточно прав для выполнения действия.")
                return redirect("catalog:home")
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
