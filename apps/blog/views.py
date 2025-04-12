from django.shortcuts import render
from django.views import View
from .models import Post
from django.http import Http404

# Create your views here.


class HomeView(View):
    def get(self, request):
        stories = Story.objects.order_by('?')[:3]
        return render(request, 'home.html', {'stories': stories})

class StoriesView(View):
    def get(self, request):
        stories = Story.objects.all()
        return render(request, 'stories.html', {'stories': stories})

class StoryDetailView(View):
    def get(self, request, slug):
        try:
            story = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404("Story not found")
        
        return render(request, 'story_detail.html', {'story': story})