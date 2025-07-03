from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model

class MyAccountAdapter(DefaultAccountAdapter):
    pass  # You can customize this if needed.

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If the user is already authenticated, do nothing
        if request.user.is_authenticated:
            return

        email = sociallogin.account.extra_data.get('email')
        if not email:
            return

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            # Link social account to existing user
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
