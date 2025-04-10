from django.shortcuts import render
from django.views import View
from .models import Story
from django.http import Http404

# Create your views here.


class HomeView(View):
    def get(self, request):
        stories = Story.objects.all()
        return render(request, 'home.html', {'stories': stories})     

class StoryDetailView(View):
    def get(self, request, slug):
        try:
            story = Story.objects.get(slug=slug)
        except Story.DoesNotExist:
            raise Http404("Story not found")
        
        return render(request, 'story_detail.html', {'story': story})