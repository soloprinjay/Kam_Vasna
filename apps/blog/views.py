from django.shortcuts import render
from django.core.paginator import Paginator
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.views import View
from .models import Post, Category
from django.http import Http404


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

        return render(request, 'story_detail.html', {'story': story})