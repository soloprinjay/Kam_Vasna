from django.urls import path
from apps.users.views import RegisterView , LoginView, ForgotPasswordView,ResetPasswordView,logout_view

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('logout/', logout_view, name='logout'),

]