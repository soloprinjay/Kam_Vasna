from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout

# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgot_password.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'reset_password.html')


def logout_view(request):
    logout(request)
    return redirect('login')