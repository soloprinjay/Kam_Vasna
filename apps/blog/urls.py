from django.urls import path

from .views import StoryDetailView, PostLikeView, SearchView, SearchSuggestionsView, DeleteCommentView

app_name = 'blog'  # <--- This is what registers the namespace!

urlpatterns = [
    path('story/<slug:slug>/', StoryDetailView.as_view(), name='story_detail'),
    path('like/<int:post_id>/', PostLikeView.as_view(), name='post_like'),
    path('comment/delete/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('search/', SearchView.as_view(), name='search'),
    path('api/search/suggestions/', SearchSuggestionsView.as_view(), name='search_suggestions'),
]
