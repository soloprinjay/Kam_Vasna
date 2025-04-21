from django.urls import path
from .views import  ContactView, RegisterView, LoginView, ForgotPasswordView, ResetPasswordView
from apps.blog.views import HomeView, StoriesView

app_name = 'dashboard'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('stories',StoriesView.as_view(),name='stories'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('forgot-password/',ForgotPasswordView.as_view(),name='forgot_password'),
    path('reset-password/',ResetPasswordView.as_view(),name='reset_password'),
]
