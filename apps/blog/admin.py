from django.contrib import admin
from .models import Category, Post, Comment, Story


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_on', 'last_modified')
    list_filter = ('category', 'created_on', 'last_modified')
    search_fields = ('title', 'category__name', 'description')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category']
    readonly_fields = ('created_on', 'last_modified')
    fieldsets = (
        ('Basic Information', {'fields': ('title', 'slug', 'category', 'description', 'image')}),
        ('Metadata', {'fields': ('created_on', 'last_modified', 'ratings', 'tags')}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post', 'email', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('name', 'email', 'body')
    autocomplete_fields = ['post']
    readonly_fields = ('created', 'updated')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'read_time', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)  