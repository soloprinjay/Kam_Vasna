from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import Post, Category, Comment


# Create your views here.


class HomeView(View):
    def get(self, request):
        stories = Post.objects.order_by('?')[:3]
        return render(request, 'home.html', {'stories': stories})


class StoriesView(View):
    def get(self, request):
        category = request.GET.get('category')
        tag = request.GET.get('tag')
        trending = request.GET.get('trending')
        search_query = request.GET.get('q', '').strip()
        page_number = request.GET.get('page', 1)

        stories = Post.objects.all()

        # Apply search filter if query exists
        if search_query:
            stories = stories.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        # Apply other filters
        if category:
            stories = stories.filter(category__name=category)
        if tag:
            stories = stories.filter(tags__name=tag)
        if trending:
            stories = stories.filter(is_trending=True).order_by('-trending_score')

        # Default ordering by creation date (newest first)
        if not trending:
            stories = stories.order_by('-created_on')

        paginator = Paginator(stories, 3)  # Show 3 stories per page
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()

        # Get all tags for search suggestions
        all_tags = []
        for story in Post.objects.all():
            all_tags.extend([tag.name for tag in story.tags.all()])
        all_tags = list(set(all_tags))  # Remove duplicates

        return render(request, 'stories.html', {
            'stories': page_obj,
            'categories': categories,
            'selected_category': category,
            'selected_tag': tag,
            'is_trending': trending,
            'search_query': search_query,
            'all_tags': all_tags,
            'total_results': stories.count()
        })


class SearchView(View):
    """Advanced search view with multiple filters and sorting options"""

    def get(self, request):
        # Get search parameters
        search_query = request.GET.get('q', '').strip()
        category = request.GET.get('category')
        tag = request.GET.get('tag')
        sort_by = request.GET.get('sort', 'newest')  # newest, oldest, popular, trending
        page_number = request.GET.get('page', 1)

        stories = Post.objects.all()

        # Apply search filter
        if search_query:
            stories = stories.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        # Apply category filter
        if category:
            stories = stories.filter(category__name=category)

        # Apply tag filter
        if tag:
            stories = stories.filter(tags__name=tag)

        # Apply sorting
        if sort_by == 'oldest':
            stories = stories.order_by('created_on')
        elif sort_by == 'popular':
            stories = stories.order_by('-likes', '-hit_count_generic__hits')
        elif sort_by == 'trending':
            stories = stories.filter(is_trending=True).order_by('-trending_score')
        else:  # newest (default)
            stories = stories.order_by('-created_on')

        # Pagination
        paginator = Paginator(stories, 6)  # Show 6 stories per page for search results
        page_obj = paginator.get_page(page_number)

        # Get all categories and tags for filters
        categories = Category.objects.all()
        all_tags = []
        for story in Post.objects.all():
            all_tags.extend([tag.name for tag in story.tags.all()])
        all_tags = list(set(all_tags))

        # Get search suggestions based on current query
        search_suggestions = []
        if search_query:
            # Get titles that contain the search query
            title_suggestions = Post.objects.filter(
                title__icontains=search_query
            ).values_list('title', flat=True)[:5]

            # Get category suggestions
            category_suggestions = Category.objects.filter(
                name__icontains=search_query
            ).values_list('name', flat=True)[:3]

            # Get tag suggestions
            tag_suggestions = [tag for tag in all_tags if search_query.lower() in tag.lower()][:3]

            search_suggestions = {
                'titles': title_suggestions,
                'categories': category_suggestions,
                'tags': tag_suggestions
            }

        return render(request, 'search_results.html', {
            'stories': page_obj,
            'categories': categories,
            'all_tags': all_tags,
            'search_query': search_query,
            'selected_category': category,
            'selected_tag': tag,
            'sort_by': sort_by,
            'total_results': stories.count(),
            'search_suggestions': search_suggestions,
            'has_results': stories.exists()
        })


class SearchSuggestionsView(View):
    """API view for search suggestions"""

    def get(self, request):
        query = request.GET.get('q', '').strip()

        if not query or len(query) < 2:
            return JsonResponse({'suggestions': []})

        suggestions = []

        # Get title suggestions
        title_suggestions = Post.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True)[:3]

        for title in title_suggestions:
            suggestions.append({
                'type': 'title',
                'text': title
            })

        # Get category suggestions
        category_suggestions = Category.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:2]

        for category in category_suggestions:
            suggestions.append({
                'type': 'category',
                'text': category
            })

        # Get tag suggestions
        all_tags = []
        for story in Post.objects.all():
            all_tags.extend([tag.name for tag in story.tags.all()])
        all_tags = list(set(all_tags))

        tag_suggestions = [tag for tag in all_tags if query.lower() in tag.lower()][:2]

        for tag in tag_suggestions:
            suggestions.append({
                'type': 'tag',
                'text': f'#{tag}'
            })

        return JsonResponse({
            'suggestions': suggestions[:8]  # Limit to 8 suggestions total
        })


class StoryDetailView(View):
    def get(self, request, slug):
        try:
            story = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404("Story not found")

        hit_count = get_hitcount_model().objects.get_for_object(story)
        HitCountMixin.hit_count(request, hit_count)

        recent_posts = Post.objects.exclude(id=story.id).order_by('-created_on')[:3]

        # Get comments for the story
        comments = story.comments.all().order_by('-timestamp')

        return render(request, 'story_detail.html', {
            'story': story,
            'recent_posts': recent_posts,
            'comments': comments
        })


class PostLikeView(View):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        try:
            post = Post.objects.get(id=post_id)
            if post.liked_by.filter(id=request.user.id).exists():
                return JsonResponse({'likes': post.likes, 'liked': True, 'error': 'Already liked'})
            post.likes += 1
            post.liked_by.add(request.user)
            post.save()
            return JsonResponse({'likes': post.likes, 'liked': True})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)


class DeleteCommentView(LoginRequiredMixin, View):
    """View to delete a comment - users can only delete their own comments"""

    def post(self, request, comment_id):
        try:
            comment = get_object_or_404(Comment, id=comment_id)

            # Check if the user owns this comment
            if comment.user != request.user:
                return JsonResponse({
                    'error': 'You can only delete your own comments'
                }, status=403)

            # Store comment info for WebSocket notification
            comment_data = {
                'id': comment.id,
                'post_id': comment.post.id
            }

            # Delete the comment
            comment.delete()

            return JsonResponse({
                'success': True,
                'message': 'Comment deleted successfully',
                'comment_id': comment_id
            })

        except Comment.DoesNotExist:
            return JsonResponse({
                'error': 'Comment not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': f'An error occurred: {str(e)}'
            }, status=500)
