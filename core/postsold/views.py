# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import ReplyForm
from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm  # Renamed from TweetForm to PostForm
from .models import Post  # Renamed from Tweet to Post
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Profile
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Post, Reply  # Renamed from Tweet to Post
from .forms import PostForm, ReplyForm
import random
import string
from django.http import HttpResponse
import openai
from django.shortcuts import render
from django.contrib.auth.models import User

openai.api_key = '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'
messages = [{"role": "system", "content": "You are an intelligent assistant."}]


def generate_ai_content1(length=3):
    # Generate a random string of specified length
    s = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return str(s)


def searchgpt(message):
    print("searching gpt")
    if message:
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


def profile_view(request, username):
    # Your profile view logic here
    # You can retrieve the user with the provided username and render the profile page
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        user = None

    return render(request, 'posts/profile.html', {'user': user})


def generate_ai_content(request):
    try:
        global messages
        # Get the post's content from the query parameter
        post_content = request.GET.get("post_content")
        ai_generated_content = searchgpt(post_content)
        if "<td>SESSION_EXPIRE_AT_BROWSER_CLOSE</td> <td class='code'><pre>False</pre></td>        </tr>              <tr>          <td>SESSION_FILE_PATH</td>    " in ai_generated_content:
            return "error can't connect to ChatGPT, please try again"
        return HttpResponse(ai_generated_content)
    except Exception as e:
        return "error connecting to ChatGPT, please try again" + "\n" + str(e)


def get_new_content2(request):
    # Logic to fetch new content from models or other sources
    new_content = "New content fetched from models or views."
    return HttpResponse('no post')


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    replies = Reply.objects.filter(post=post)

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.save()
            return redirect('post_detail', post_id=post_id)
    else:
        reply_form = ReplyForm()

    context = {
        'post': post,
        'replies': replies,
        'user': request.user,  # Pass the user object to the template context
    }
    return render(request, 'posts/post_detail.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')  # Redirect to the post list page
        else:
            # Handle invalid login
            return render(request, 'posts/login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'postss/login.html')


def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'profile.html', context)


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    total_score = 0  # Initialize total score
    for post in posts:
        post.score = post.likes.count() + post.retweets.count() * 2 - post.dislikes.count()
        total_score += post.score
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associate the post with the current user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    context = {'posts': posts, 'form': form, 'total_score': total_score}
    return render(request, 'posts/post_list.html', context)


def reply_list_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    replies = post.replies.filter(parent_reply__isnull=True)  # Only top-level replies

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply_form.cleaned_data['content'] = 'New content for the reply'
            new_reply = reply_form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.parent_reply = None  # Top-level reply
            new_reply.save()
            return redirect('post_detail', post_id=post_id)
    else:
        reply_form = ReplyForm()

    context = {'post': post, 'replies': replies, 'reply_form': reply_form}
    return render(request, 'posts/post_detail.html', context)


@login_required
def like_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    user = request.user

    if user.is_authenticated:
        if user in reply.likes.all():
            reply.likes.remove(user)
        else:
            reply.likes.add(user)
            if user in reply.dislikes.all():
                reply.dislikes.remove(user)
    else:
        # Handle the case when the user is not authenticated
        pass

    return redirect('post_detail', post_id=reply.post.id)


@login_required
def dislike_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    user = request
