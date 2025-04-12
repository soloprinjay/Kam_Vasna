from django.shortcuts import render
from django.views import View
from .models import Post
from django.http import Http404


# Create your views here.


class HomeView(View):
    def get(self, request):
        stories = Post.objects.order_by('?')[:3]
        return render(request, 'home.html', {'stories': stories})

class StoriesView(View):
    def get(self, request):
        category = request.GET.get('category')
        if category:
            stories = Story.objects.filter(category=category)
        else:
            stories = Story.objects.all()

        categories = [c[0] for c in Story.CATEGORY_CHOICES]
        return render(request, 'stories.html', {
            'stories': stories,
            'categories': categories,
            'selected_category': category
        })

class StoryDetailView(View):
    def get(self, request, slug):
        try:
            story = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404("Story not found")
        
        return render(request, 'story_detail.html', {'story': story})