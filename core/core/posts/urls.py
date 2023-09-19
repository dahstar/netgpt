from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='post_list'),  # Updated to use 'home_view'
    path('register/', views.register, name='register'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),  # Updated to use 'delete_post'
    path('login/', views.login_view, name='login'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='post_list'), name='logout'),  # Updated to use 'post_list'
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),  # Updated to use 'post_detail'
    path('get_new_content/', views.generate_ai_content, name='generate_ai_content'),
    path('posts/<int:post_id>/replies/', views.reply_list_view, name='reply_list_view'),  # Updated to use 'reply_list_view'
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
    path('create/', views.create_post, name='create_post'),  # Updated to use 'create_post'
    path('like/<int:post_id>/', views.like_post, name='like_post'),  # Updated to use 'like_post'
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),  # Updated to use 'dislike_post'
    path('reposts/<int:post_id>/', views.repost_post, name='repost_post'),  # Updated to use 'repost_post'
    path('accounts/profile/', views.profile, name='profile'),  # Updated to use 'profile'
    path('search/', views.search_posts, name='search_posts'),
    path('filter_posts/', views.filter_posts, name='filter_posts'),
    path('sort_posts/', views.sort_posts, name='sort_posts'),

]
