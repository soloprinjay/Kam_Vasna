from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import secrets

User = get_user_model()
# Function to generate and send a random password
def set_random_password_and_send_email(user,request):
    random_password = secrets.token_urlsafe(10)  # generates a strong password
    user.set_password(random_password)  # This is still valid even if the password field is CharField
    user.save()

    login(request, user)

    # Render the HTML template
    html_message = render_to_string('email/password_reset_email.html', {
        'user': user,
        'random_password': random_password
    })
    
    # Create plain text version
    plain_message = strip_tags(html_message)

    send_mail(
        subject="आपका नया पासवर्ड",
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message
    )

def send_password_reset_link_email(user, reset_url):
    subject = "पासवर्ड रीसेट लिंक"
    html_message = render_to_string('email/password_reset_link_email.html', {
        'user': user,
        'reset_url': reset_url
    })
    send_mail(
        subject=subject,
        message=f"पासवर्ड रीसेट करने के लिए यह लिंक खोलें: {reset_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message
    )
