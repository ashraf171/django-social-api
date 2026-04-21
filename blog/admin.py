from django.contrib import admin
from .models import User, Post, Comment, Like, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'email',
        'followers_count',
        'following_count',
        'is_staff',
    ]
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'title',
        'likes_count',
        'created_at',
        'updated_at',
    ]
    search_fields = ['title', 'content', 'author__username']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'post',
        'parent',
        'created_at',
        'updated_at',
    ]
    search_fields = ['content', 'author__username', 'post__title']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post']
    search_fields = ['author__username', 'post__title']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']
    list_filter = ['created_at']
    ordering = ['-created_at']