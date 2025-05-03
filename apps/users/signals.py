from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from apps.users.utils import set_random_password_and_send_email


# Signal receiver for user login
@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    # Check if the user logged in via Google
    if user.socialaccount_set.filter(provider='google').exists():
        set_random_password_and_send_email(user)  # Generate and send the random password
