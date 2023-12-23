from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    postBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_by')
    postContent = models.TextField()
    postDate = models.DateTimeField(auto_now_add=True)
    postLikes = models.IntegerField(default=0)
    likedBy = models.ManyToManyField(User, related_name='liked_by', blank=True)

    def __str__(self):
        return f"Posted by: {self.postBy}, Date: {self.postDate}, Likes: {self}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"Follower: {self.follower}, Following: {self.following}"
