#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import ReplyForm
from django.shortcuts import render, redirect,get_object_or_404
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Profile
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Post, Reply
from .forms import PostForm, ReplyForm
import random
import string
from django.http import HttpResponse
import openai
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Count,ExpressionWrapper, IntegerField
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import models
from django.http import HttpResponseRedirect
try:
 import sys
 sys.path.append('/home/kali/Desktop/')

 from  config_local import config

except Exception as e:
  pass



openai.api_key = config("openai", default="123")
messages = [ {"role": "system", "content": 
              "You are a intelligent assistant."} ]
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    total_score = 0
    for post in posts:
        post.score = post.likes.count() + post.reposts.count() * 2 - post.dislikes.count()
        total_score += post.score
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associate the post with the current user
             
            post.save()
            return redirect('post_list')
        else:
                form = PostForm()
      

    context = {'posts': posts, 'total_score': total_score}
    return render(request, 'posts/post_list.html', context)

def sort_posts(request):
    sort_by_time = request.GET.get('sort_by_time', 'false')
    sort_by_time = sort_by_time.lower() == 'false'

    if sort_by_time:
        posts = Post.objects.all().order_by('-created_at')
    else:
        posts = Post.objects.all().annotate(score=F('likes__count') + F('reposts__count') * 2 - F('dislikes__count')).order_by('-score')

    context = {'posts': posts}
    post_list_html = render_to_string('posts/includes/post_list.html', context)
    return JsonResponse({'sorted_posts': post_list_html})
def search_posts(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')  # Get the search query from the request
        
        # Implement your search logic here (e.g., using filters)
        matching_posts = Post.objects.filter(content__icontains=query)
        
        # Create a list of post data
        results = [{'content': post.content, 'created_at': post.created_at} for post in matching_posts]
        
        return JsonResponse({'results': results})
def generate_ai_content1(length=3):
    # Generate a random string of specified length
    s= ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return  str(s)
def filter_posts(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')

        # Use Q objects to search for posts containing the search term in content
        filtered_posts = Post.objects.filter(Q(content__icontains=search_term))

        # Render a template to display the filtered posts
        return render(request, 'posts/filtered_posts.html', {'filtered_posts': filtered_posts})

    return HttpResponse('Invalid request method', status=400)
def searchgpt(message):
   print("searching gpt")  
   if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
         
        messages.append({"role": "assistant", "content": reply})
        return reply
def profile_view(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    context = {
        'user_profile': user,
    }
    return render(request, 'profile.html', context)
def generate_ai_content(request):
  try:
    global messages
      
    # Get the post's content from the query parameter
    post_content = request.GET.get("post_content")
    
    ai_generated_content =searchgpt(post_content)
    if  "<td>SESSION_EXPIRE_AT_BROWSER_CLOSE</td>          <td class='code'><pre>False</pre></td>        </tr>              <tr>          <td>SESSION_FILE_PATH</td>    " in ai_generated_content:
                return "error can't connect chatgpt try again"
    return HttpResponse(ai_generated_content)
  except Exception as e :
         print(str(e))
         return "error on connection to chatgpt try again"+"\n"+str(e)

def get_new_content2(request):
    # Logic to fetch new content from models or other sources
    new_content = "New content fetched from models or views."

    return  HttpResponse('no post')
 
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
    
    return render(request, 'posts/login.html')
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
    # Default sort order is by date
    sort_order = request.session.get('sort_order', '-created_at')

    if request.method == 'POST':
        # Handle form submission for creating a new post
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    # Toggle sorting order between date and score
    if sort_order == '-created_at':
        sort_order = '-likes'  # Change this to the appropriate field for score
    else:
        sort_order = '-created_at'

    # Update the session variable with the current sorting order
    request.session['sort_order'] = sort_order

    # Retrieve and sort the posts
    if sort_order == '-likes':
        posts = Post.objects.all().annotate(score=models.Count('likes')).order_by(sort_order)
    else:
        posts = Post.objects.all().order_by(sort_order)

    context = {'posts': posts, 'form': form}
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
    user = request.user

    if user.is_authenticated:
        if user in reply.dislikes.all():
            reply.dislikes.remove(user)
        else:
            reply.dislikes.add(user)
            if user in reply.likes.all():
                reply.likes.remove(user)
    else:
        # Handle the case when the user is not authenticated
        pass

    return redirect('post_detail', post_id=reply.post.id)

@login_required
def repost_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    user = request.user

    if user.is_authenticated:
        if user in reply.reposts.all():
            reply.reposts.remove(user)
        else:
            reply.reposts.add(user)
    else:
        # Handle the case when the user is not authenticated
        pass

    return redirect('post_detail', post_id=reply.post.id)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')  # Redirect after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
def home_view(request):
    posts = Post.objects.all()
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_detail')
    else:
        form = PostForm()
    
    context = {'posts': posts, 'form': form}  # Include the 'form' variable
    return render(request, 'posts/post_detail.html', context)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.user == post.user or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('post_list')
        context = {'post': post}
        return render(request, 'delete_post.html', context)
    else:
         context = {}
         return render(request, 'posts/logs/notauthorized.html', context) 
        #raise PermissionDenied
@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    post_id = reply.post.id  # Store the post ID before deleting the reply
    if reply.user == request.user or request.user.is_superuser:
        reply.delete()
    return redirect('post_detail', post_id=post_id)
 

 

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Set the user field to the currently logged-in user
            post.save()
            return redirect('post_list')  # Redirect to the home page or wherever you want
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'posts/create_post.html', context)
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user.is_authenticated:
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            if user in post.dislikes.all():
                post.dislikes.remove(user)
    else:
        # Handle the case when the user is not authenticated
        # You can redirect them to the login page or show an error message
        pass
    context={}
    return redirect('post_list')



@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user.is_authenticated:
        if user in post.dislikes.all():
            post.dislikes.remove(user)
        else:
            post.dislikes.add(user)
            if user in post.likes.all():
                post.likes.remove(user)
    else:
        # Handle the case when the user is not authenticated
        # You can redirect them to the login page or show an error message
        pass

    # Return a redirect response to the home view
    return redirect('post_list')


@login_required
def repost_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user.is_authenticated:
        if user in post.reposts.all():
            post.reposts.remove(user)
        else:
            post.reposts.add(user)
    else:
        # Handle the case when the user is not authenticated
        # You can redirect them to the login page or show an error message
        pass

    context = {'posts': posts, 'form': form}
    return render(request, 'posts/post_list.html', context)
  





def home_view(request):
    posts = Post.objects.all()
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.user = request.user  
            form.save()
            return redirect('post_list')  # Redirect to the post list page after creating a post
    else:
        form = PostForm()
    
    context = {'posts': posts, 'form': form}
    return render(request, 'posts/post_list.html', context)
