import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow, PostLike


def index(request):
    all_posts = Post.objects.all().order_by('-postDate')
    paginator = Paginator(all_posts, 10)
    page_num = request.GET.get('page')
    page_posts = paginator.get_page(page_num)

    user_likes = []
    all_likes = PostLike.objects.all()
    try:
        for like in all_likes:
            if like.likedBy == request.user:
                user_likes.append(like.likedPost.id)
    except:
        user_likes = []
    if request.method == 'POST':
        post_content = request.POST['post-content']

        if post_content:
            user = User.objects.get(pk=request.user.id)
            new_post = Post(postAuther=user, postContent=post_content)
            new_post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {
                'message': 'Please enter a character!!!',
                'all_posts': all_posts,
                'page_posts': page_posts,
                'user_likes': user_likes,
            }
            return render(request, 'network/index.html', context=context)
    return render(request, "network/index.html",
                  context={
                      'all_posts': all_posts,
                      'page_posts': page_posts,
                      'user_likes': user_likes,
                  })


@login_required
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = PostLike(likedBy=user, likedPost=post)
    like.save()
    post.postLikes += 1
    post.save()
    return JsonResponse({'liked': True})


@login_required
def unlike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = PostLike.objects.filter(likedBy=user, likedPost=post)
    like.delete()
    post.postLikes -= 1
    post.save()
    return JsonResponse({'unliked': True})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(postAuther=user).order_by('-postDate')
    paginator = Paginator(all_posts, 10)
    page_num = request.GET.get('page')
    page_posts = paginator.get_page(page_num)
    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)
    is_follow = followers.filter(follower=User.objects.get(pk=request.user.id))
    user_likes = []
    all_likes = PostLike.objects.all()
    try:
        for like in all_likes:
            if like.likedBy == request.user:
                user_likes.append(like.likedPost.id)
    except:
        user_likes = []
    context = {
        'name': user,
        'all_posts': all_posts,
        'page_posts': page_posts,
        'followers': followers,
        'following': following,
        'is_follow': is_follow,
        'user_likes': user_likes,
    }
    return render(request, "network/profile.html",
                  context=context
                  )


@login_required
def follow(request):
    c_user = request.POST["c_user"]
    current_user = User.objects.get(pk=request.user.id)
    c_user_info = User.objects.get(username=c_user)
    f_user = Follow(follower=current_user, following=c_user_info)
    f_user.save()
    user_id = c_user_info.id
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))


@login_required
def unfollow(request):
    c_user = request.POST["c_user"]
    current_user = User.objects.get(pk=request.user.id)
    c_user_info = User.objects.get(username=c_user)
    f_user = Follow.objects.get(follower=current_user, following=c_user_info)
    f_user.delete()
    user_id = c_user_info.id
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))


@login_required
def following(request):
    user = User.objects.get(pk=request.user.id)
    all_posts = Post.objects.all().order_by('-postDate')
    all_following = Follow.objects.filter(follower=user)
    following_posts = []
    for post in all_posts:
        for p in all_following:
            if p.following == post.postAuther:
                following_posts.append(post)

    paginator = Paginator(following_posts, 10)
    page_num = request.GET.get('page')
    page_posts = paginator.get_page(page_num)

    user_likes = []
    all_likes = PostLike.objects.all()
    try:
        for like in all_likes:
            if like.likedBy == request.user:
                user_likes.append(like.likedPost.id)
    except:
        user_likes = []

    context = {
        'name': user,
        'all_posts': all_posts,
        'page_posts': page_posts,
        'user_likes': user_likes,
    }
    return render(request, "network/following.html",
                  context=context
                  )


def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        post.postContent = data['content']
        post.save()
        return JsonResponse({'success': True, 'data': data['content']})
