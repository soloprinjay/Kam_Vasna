from django.urls import path
from .views import  ContactView
from apps.blog.views import HomeView, StoriesView
from .views import UserSubscription
app_name = 'dashboard'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('stories',StoriesView.as_view(),name='stories'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('subscription',UserSubscription.as_view(),name='subscription')
]
