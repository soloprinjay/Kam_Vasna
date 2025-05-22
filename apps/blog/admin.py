from django.contrib import admin
from .models import Category, Post, Comment


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
        ('Metadata', {'fields': ('created_on', 'likes', 'last_modified', 'ratings', 'tags')}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'timestamp')
    list_filter = ('timestamp', 'post', 'user')
    search_fields = ('body', 'user__email', 'post__title')
    readonly_fields = ('timestamp',)
    raw_id_fields = ('user', 'post')

