from django.urls import path
from .views import  ContactView, Index2View
from apps.blog.views import HomeView

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('contact/',ContactView.as_view(),name='contact'),
    path('index2',Index2View.as_view(),name='index2'),
]
