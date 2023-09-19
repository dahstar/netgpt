from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home_view,profile
 

urlpatterns = [
    path('', views.home, name='post_list'),
    path('register/', views.register, name='register'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
      path('login/', views.login_view, name='login'),  # Use your actual URL pattern here
             path('profile/<str:username>/', views.profile_view, name='profile'),

        path('logout/', auth_views.LogoutView.as_view(next_page='post_list'), name='logout'),
    path('login/', views.login_view, name='login'),  # Use your actual URL pattern here
       path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('get_new_content/', views.generate_ai_content, name='generate_ai_content'),
  
    path('post/<int:posts_id>/replies/', views.reply_list_view, name='reply_list_view'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('reposts/<int:post_id>/', views.repost_post, name='retpost_post'),
       path('accounts/profile/', profile, name='profile'),
     
]
