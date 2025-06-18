from django.urls import path
from .views import StoryDetailView, PostLikeView, SearchView, SearchSuggestionsView

app_name = 'blog'  # <--- This is what registers the namespace!


urlpatterns = [
    path('story/<slug:slug>/', StoryDetailView.as_view(), name='story_detail'),
    path('like/<int:post_id>/', PostLikeView.as_view(), name='post_like'),
    path('search/', SearchView.as_view(), name='search'),
    path('api/search/suggestions/', SearchSuggestionsView.as_view(), name='search_suggestions'),
 ]
