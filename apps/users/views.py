import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

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


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'reset_password.html')

class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'change_password.html')

    def post(self, request):
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(old_password):
            messages.error(request, 'पुराना पासवर्ड गलत है।')

        elif new_password != confirm_password:
            messages.error(request, 'नया पासवर्ड मेल नहीं खा रहा है।')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # to avoid logout
            messages.success(request, 'पासवर्ड सफलतापूर्वक बदल दिया गया है।')
            return redirect('change-password')
        return render(request, 'change_password.html')



def logout_view(request):
    logout(request)
    return redirect('users:login-user')