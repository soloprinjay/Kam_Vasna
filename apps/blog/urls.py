from django.urls import path
from .views import StoryDetailView

app_name = 'blog'  # <--- This is what registers the namespace!


urlpatterns = [
    path('story/<slug:slug>/', StoryDetailView.as_view(), name='story_detail'),
 ]
