import re
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from hitcount.models import HitCount
from star_ratings.models import Rating
from taggit.managers import TaggableManager

User = get_user_model()

from apps.users.models import CustomUser


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    description = CKEditor5Field()
    image = models.ImageField(upload_to='story_images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    ratings = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True)
    tags = TaggableManager()
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField('users.CustomUser', related_name='liked_posts', blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count')
    trending_score = models.FloatField(default=0.0)  # Score to determine trending status
    is_trending = models.BooleanField(default=False)  # Flag to mark trending stories

    def save(self, *args, **kwargs):
        if not self.slug:
            clean_title = re.sub(r'[^a-zA-Z0-9\s-]', '', self.title)  # Remove special characters
            self.slug = slugify(clean_title)  # Convert title to slug

        # Calculate trending score based on views, likes, and recency
        views = self.hit_count_generic.first().hits if self.hit_count_generic.first() else 0
        likes = self.likes
        hours_since_creation = (timezone.now() - self.created_on).total_seconds() / 3600

        # Trending score formula: (views + likes * 2) / (hours_since_creation + 2)^1.5
        self.trending_score = (views + likes * 2) / ((hours_since_creation + 2) ** 1.5)

        # Mark as trending if score is above threshold
        self.is_trending = self.trending_score > 10.0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField('users.CustomUser', related_name='liked_comments', blank=True)
    mentions = models.ManyToManyField('users.CustomUser', related_name='mentioned_in_comments', blank=True)

    def __str__(self):
        return f'{self.user} - {self.body[:20]}'
