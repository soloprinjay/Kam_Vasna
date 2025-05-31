from django.core.paginator import Paginator
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


from .models import Post, Category


# Create your views here.


class HomeView(View):
    def get(self, request):
        stories = Post.objects.order_by('?')[:3]
        return render(request, 'home.html', {'stories': stories})


class StoriesView(View):
    def get(self, request):
        category = request.GET.get('category')
        page_number = request.GET.get('page', 1)

        if category:
            stories = Post.objects.filter(category__name=category)
        else:
            stories = Post.objects.all()

        paginator = Paginator(stories, 3)  # Show 6 stories per page
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()
        return render(request, 'stories.html', {
            'stories': page_obj,
            'categories': categories,
            'selected_category': category
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

        return render(request, 'story_detail.html', {
            'story': story,
            'recent_posts': recent_posts
        })


class PostLikeView(View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)

        session_key = f"liked_post_{post_id}"
        liked = False

        if not request.session.get(session_key, False):
            post.likes += 1
            post.save()
            request.session[session_key] = True
            liked = True
        else:
            liked = False  # already liked in this session

        return JsonResponse({'liked': liked, 'likes': post.likes})
