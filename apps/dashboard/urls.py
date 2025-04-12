from django.urls import path
from .views import  ContactView
from apps.blog.views import HomeView, StoriesView

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('stories',StoriesView.as_view(),name='stories'),
    path('contact/',ContactView.as_view(),name='contact'),
]
