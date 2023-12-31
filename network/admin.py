from django.contrib import admin
from .models import User, Post, Follow, PostLike


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'postAuther', 'postDate', 'postLikes')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('likedBy', 'likedPost')
