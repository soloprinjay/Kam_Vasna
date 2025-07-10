"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from apps.blog.models import Post
from django.urls import reverse

# Sitemaps
class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['dashboard:home', 'dashboard:stories', 'dashboard:contact', 'dashboard:privacy_policy']

    def location(self, item):
        return reverse(item)

class BlogStorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated_on if hasattr(obj, 'updated_on') else obj.created_on

    def location(self, obj):
        return reverse('blog:story_detail', kwargs={'slug': obj.slug})

sitemaps = {
    'static': StaticViewSitemap,
    'stories': BlogStorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('blog/', include('apps.blog.urls')),
    path('users/', include('apps.users.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('accounts/', include('allauth.urls')),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
