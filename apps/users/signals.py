from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from apps.cart.services import merge_session_cart_to_user


@receiver(user_logged_in)
def merge_cart_after_login(sender, request, user, **kwargs):
    if request.session.session_key:
        merge_session_cart_to_user(user, request.session.session_key)
