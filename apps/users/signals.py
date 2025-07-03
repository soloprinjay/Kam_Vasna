from allauth.socialaccount.signals import social_account_added
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from apps.users.utils import set_random_password_and_send_email


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    if getattr(request, '_password_reset_done', False):
        return  # Prevent infinite recursion

    if user.socialaccount_set.filter(provider='google').exists() and not request.user.has_set_password:
        request._password_reset_done = True  # Set flag to prevent recursion
        set_random_password_and_send_email(user, request)
