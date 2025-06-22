from .models import Post

def trending_stories(request):
    """Add trending stories to the context of all templates"""
    trending_stories = Post.objects.filter(is_trending=True).order_by('-trending_score')[:5]
    return {
        'trending_stories': trending_stories
    }