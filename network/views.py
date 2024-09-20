from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow, Like



def index(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    # Add code to get the user's profile and related information
    user = request.user if request.user.is_authenticated else None
    profile_user = user
    if user:
        followers_count = Follow.objects.filter(followed=profile_user).count()
        following_count = Follow.objects.filter(follower=profile_user).count()
        is_following = Follow.objects.filter(follower=user, followed=profile_user).exists()
    else:
        followers_count = following_count = is_following = 0

    return render(request, "network/index.html", {
        "page": page,
        "posts": posts,
        "profile_user": profile_user,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })


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
        
        # Check if email, password, or confirmation are empty
        if not email or not password or not confirmation:
            return render(request, "network/register.html", {
                "message": "Please fill in all fields."
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
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post(content=content, user=user)
        post.save()
        return redirect("index")
    else:
        return render(request, "network/index.html")



@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers_count = Follow.objects.filter(followed=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    user = request.user
    is_following = Follow.objects.filter(follower=user, followed=profile_user).exists()
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')

    if request.method == 'POST':
        if request.FILES.get('profile_image'):
            profile_user.profile_image = request.FILES['profile_image']
            profile_user.save()
            messages.success(request, 'Profile image updated successfully.')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "page": page,
        "posts": posts
    })



@login_required
def follow_unfollow_user(request, username):
    followed_user = User.objects.get(username=username)
    follower = request.user

    if follower != followed_user:
        if Follow.objects.filter(follower=follower, followed=followed_user).exists():
            Follow.objects.filter(follower=follower, followed=followed_user).delete()
            following = False
        else:
            Follow.objects.create(follower=follower, followed=followed_user)
            following = True

        # Calculate updated follower and following counts
        follower_count = Follow.objects.filter(followed=followed_user).count()
        following_count = Follow.objects.filter(follower=followed_user).count()

        return JsonResponse({
            "following": following,
            "follower_count": follower_count,
            "following_count": following_count,
        })
    return JsonResponse({"error": "Invalid request"})



@login_required
def following(request):
    user = request.user
    following = Follow.objects.filter(follower=user).values_list('followed', flat=True)
    posts = Post.objects.filter(user__in=following).order_by('-created_at')

    user = request.user if request.user.is_authenticated else None
    profile_user = user
    if user:
        followers_count = Follow.objects.filter(followed=profile_user).count()
        following_count = Follow.objects.filter(follower=profile_user).count()
        is_following = Follow.objects.filter(follower=user, followed=profile_user).exists()
    else:
        followers_count = following_count = is_following = 0

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page": page,
        "posts": posts,
        "profile_user": profile_user,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        })


@csrf_exempt
@login_required(redirect_field_name='my_redirect_field')
def edit_post(request, post_id):
        post = Post.objects.get(pk=post_id)

        if request.method == 'POST':
            data = json.loads(request.body)
            new_content = data.get("content")

            post.content = new_content
            post.save()

            return JsonResponse({"status": "success", "new_content": new_content})
        

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if post.likes.filter(pk=user.pk).exists():
        # User has already liked the post, so unlike it
        like = Like.objects.get(post=post, user=user)
        like.delete()
        post.likes.remove(user)
        liked = False
    else:
        # User hasn't liked the post, so like it
        like = Like(post=post, user=user)
        like.save()
        post.likes.add(user)
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})



@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user attempting to delete the post is the post's author
    if request.user == post.user:
        post.delete()
        return JsonResponse({'deleted': True})
    else:
        return JsonResponse({'deleted': False})

