from django.urls import path
from .views import StoryDetailView


urlpatterns = [
    path('story/<slug:slug>/', StoryDetailView.as_view(), name='story_detail'),
 ]
