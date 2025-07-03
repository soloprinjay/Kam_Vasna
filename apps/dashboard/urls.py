from django.urls import path

from apps.blog.views import HomeView, StoriesView
from .views import ContactView
from .views import UserSubscription, PrivacyPolicyView

app_name = 'dashboard'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('stories', StoriesView.as_view(), name='stories'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('subscription', UserSubscription.as_view(), name='subscription'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]
