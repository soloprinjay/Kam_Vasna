import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db.models import Q

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
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user = request.user
            old_password = data.get('current_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

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











