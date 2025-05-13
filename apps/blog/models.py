from django.db import models
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from star_ratings.models import Rating
from django.utils.text import slugify
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from apps.users.models import CustomUser
import re


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
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count')


    def save(self, *args, **kwargs):
        if not self.slug:
            clean_title = re.sub(r'[^a-zA-Z0-9\s-]', '', self.title)  # Remove special characters
            self.slug = slugify(clean_title)  # Convert title to slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField('users.CustomUser', related_name='liked_comments', blank=True)

    def __str__(self):
        return f'{self.user} - {self.body[:20]}'




