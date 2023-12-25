from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    postAuther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_by')
    postContent = models.CharField(max_length=250)
    postDate = models.DateTimeField(auto_now_add=True)
    postLikes = models.IntegerField(default=0)
    # likedBy = models.ManyToManyField(User, blank=True, related_name='liked_by')

    def __str__(self):
        return (f"{self.id}, Posted by: {self.postAuther}, Date: {self.postDate},"
                f" Likes: {self.postLikes}")


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"Follower: {self.follower}, Following: {self.following}"


class PostLike(models.Model):
    likedPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likedPost')
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likedBy')

    def __str__(self):
        return f"User: {self.likedBy}, Post: {self.likedPost}"