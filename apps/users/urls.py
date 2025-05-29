from django.urls import path
from apps.users.views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView, logout_view, \
    ChangePasswordView, post_login_redirect, UpdateProfileView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login-user'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('post-login-redirect/', post_login_redirect, name='post-login-redirect'),
    path('logout/', logout_view, name='logout-user'),
    path('api/users/suggestions/', views.user_suggestions, name='user_suggestions'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
]
