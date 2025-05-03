from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets

User = get_user_model()
# Function to generate and send a random password
def set_random_password_and_send_email(user):
    random_password = secrets.token_urlsafe(10)  # generates a strong password
    user.set_password(random_password)  # This is still valid even if the password field is CharField
    user.save()
    send_mail(
        subject="Your new password",
        message=f"Hello {user.email},\n\nHere is your password: {random_password}\n\nPlease change it after logging in.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
