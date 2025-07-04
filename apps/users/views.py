import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from apps.users.models import CustomUser

User = get_user_model()


# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm-password')
            terms_of_use = data.get('terms')

            if not all([full_name, email, password, confirm_password, terms_of_use]):
                return JsonResponse({'success': False, 'message': 'All fields are required.'})

            if password != confirm_password:
                return JsonResponse({'success': False, 'message': 'Passwords do not match.'})

            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email is already registered.'})

            User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                terms_confirmed=terms_of_use
            )

            return JsonResponse({'success': True, 'message': 'Registration successful.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        body = json.loads(request.body)

        email = body.get('email')
        password = body.get('password')
        remember_me = body.get('remember_me')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
            else:
                request.session.set_expiry(0)

            return JsonResponse({'success': True, 'redirect_url': '/'})  # Home page

        else:
            return JsonResponse({'success': False, 'message': 'ईमेल या पासवर्ड गलत है।'})


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f"/users/reset-password/?uid={uid}&token={token}"
            )
            # Render email template
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
            messages.success(request, 'पासवर्ड रीसेट लिंक आपके ईमेल पर भेज दिया गया है।')
        else:
            messages.error(request, 'यह ईमेल हमारे रिकॉर्ड में नहीं है।')
        return render(request, 'forgot_password.html')


class ResetPasswordView(View):
    def get(self, request):
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')
        context = {'validlink': False}
        if uidb64 and token:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            token_generator = PasswordResetTokenGenerator()
            if user and token_generator.check_token(user, token):
                context['validlink'] = True
                context['uid'] = uidb64
                context['token'] = token
        return render(request, 'reset_password.html', context)

    def post(self, request):
        uidb64 = request.POST.get('uid')
        token = request.POST.get('token')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        context = {'validlink': False}
        if not (uidb64 and token):
            messages.error(request, 'लिंक अमान्य है।')
            return render(request, 'reset_password.html', context)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        token_generator = PasswordResetTokenGenerator()
        if user and token_generator.check_token(user, token):
            if not password or not confirm_password:
                messages.error(request, 'कृपया सभी फ़ील्ड भरें।')
                context['validlink'] = True
                context['uid'] = uidb64
                context['token'] = token
                return render(request, 'reset_password.html', context)
            if password != confirm_password:
                messages.error(request, 'पासवर्ड मेल नहीं खा रहे हैं।')
                context['validlink'] = True
                context['uid'] = uidb64
                context['token'] = token
                return render(request, 'reset_password.html', context)
            user.set_password(password)
            user.has_set_password = True
            user.save()
            messages.success(request, 'पासवर्ड सफलतापूर्वक बदल दिया गया है। अब आप लॉगिन कर सकते हैं।')
            return redirect('users:login-user')
        else:
            messages.error(request, 'लिंक अमान्य या समाप्त हो गया है।')
        return render(request, 'reset_password.html', context)


class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'change_password.html')

    def post(self, request):
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user = request.user
            old_password = data.get('current_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if old_password == new_password:
                return JsonResponse({'message': 'नया पासवर्ड पुराने पासवर्ड जैसा नहीं हो सकता।'}, status=400)

            if not user.check_password(old_password):
                return JsonResponse({'message': 'पुराना पासवर्ड गलत है।'}, status=400)

            if new_password != confirm_password:
                return JsonResponse({'message': 'नया पासवर्ड मेल नहीं खा रहा है।'}, status=400)

            user.set_password(new_password)
            user.has_set_password = True
            user.save()
            update_session_auth_hash(request, user)

            return JsonResponse({'message': 'पासवर्ड सफलतापूर्वक बदल दिया गया है।'})

        return JsonResponse({'message': 'Invalid request.'}, status=400)


def logout_view(request):
    logout(request)
    return redirect('users:login-user')


@login_required
def post_login_redirect(request):
    user = request.user
    if not user.has_set_password:
        messages.success(request, "Please check your email, we have sent you your new password")
        return redirect('/')
    return redirect('/')  # or wherever you want users to go normally


def user_suggestions(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'users': []})

    User = get_user_model()
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )[:5]  # Limit to 5 suggestions

    suggestions = [{
        'id': user.id,
        'name': user.get_full_name() or user.email,
        'username': user.username
    } for user in users]

    return JsonResponse({'users': suggestions})


class UpdateProfileView(View):
    def get(self, request):
        return render(request, 'update_profile.html')

    def post(self, request):
        user = request.user
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        self_info = request.POST.get('bio', '').strip()

        # Update user fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.self_info = self_info
        user.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('users:update_profile')  # Use your appropriate URL name
