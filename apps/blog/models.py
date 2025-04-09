from django.db import models
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from star_ratings.models import Rating
from django.utils.text import slugify
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

    def save(self, *args, **kwargs):
        if not self.slug:
            clean_title = re.sub(r'[^a-zA-Z0-9\s-]', '', self.title)  # Remove special characters
            self.slug = slugify(clean_title)  # Convert title to slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name      


class Story(models.Model):
    CATEGORY_CHOICES = [
        ('लोककथा', 'लोककथा'),
        ('ऐतिहासिक', 'ऐतिहासिक'),
        ('प्रेरक', 'प्रेरक'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image_url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()
    read_time = models.IntegerField(help_text="Minutes to read")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

