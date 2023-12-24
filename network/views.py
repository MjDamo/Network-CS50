import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    blog = Post.objects.all()
    blog = blog[::-1]
    paginator = Paginator(blog, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)
    if request.method == 'POST':
        post_content = request.POST['post-content']

        if post_content:
            user = User.objects.get(pk=request.user.id)
            new_post = Post(postAuther=user, postContent=post_content)
            new_post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {
                'massage': 'Please enter a character!!!',
                'page_object': page_object,
            }
            return render(request, 'network/index.html', context=context)
    return render(request, "network/index.html",
                  context={'page_object': page_object})


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


@login_required
@csrf_exempt
def post_edit(request, post_id):
    if request.method == "POST":
        json_info = json.loads(request.body)
        content = json_info.get('content')
        if content and content.strip():
            blog = Post.objects.filter(id=post_id)
            blog.update(content=content)
            return JsonResponse(data={'massage': 'updated'}, status=201)
        return JsonResponse(data={'massage': 'error'}, status=201)
    if request.user == request.user:
        return JsonResponse(data={'massage': 'Accepted'}, status=201)
    return JsonResponse(data={'massage': 'Rejected'}, status=201)


def posts(request):
    blog = Post.objects.all()
    blog = blog[::-1]
    paginator = Paginator(blog, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'network/posts.html', context=context)


@login_required
def follow_posts(request):
    author = request.user.username
    user = User.objects.get(username=author)
    follow = user.following.all()
    blog = []
    for person in follow:
        posts = person.following.posted_by.all()
        for post in posts:
            blog.insert(0, post)
    if blog:
        blog = sorted(blog, key=lambda post: post.postBy, reverse=True)
        paginator = Paginator(blog, 10)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        context = {'page_obj': page_obj}
        return render(request, "network/posts.html", context=context)
    context = {
        'Message': 'You are not following any one, please follow other to see their posts!!!'
    }
    return render(request, 'network/posts.html', context=context)

@login_required
def like_posts(request, post_id=None):
    try:
        post = Post.objects.get(pk=post_id)
        author = User.objects.get(pk=request.user.id)
        liked_by = post.liked.all()
    except:
        return JsonResponse({
            'error': 'nothing here!!'
        }, status=201)
    flag = True
    for liked in liked_by:
        if liked.author == author:
            post.liked.remove(author)
            if post.likedBy >= 1:
                post.likedBy -= 1
                post.save()
                flag = False
                return JsonResponse({
                    'likeCounter': post.likedBy,
                }, status=200)
    if flag:
        post.liked.add(author)
        post.likedBy += 1
        post.save()
        return JsonResponse({
            'likeCounter': post.likedBy
        }, status=200)
    return JsonResponse({
        'error': 'nothing there!!'
    })
