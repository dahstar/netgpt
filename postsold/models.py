from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    reposts= models.ManyToManyField(User, related_name='reposts_posts', blank=True)
    ai_generated_content = models.TextField(blank=True, null=True)
 
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_replies', blank=True)
    repost= models.ManyToManyField(User, related_name='reposted_replies', blank=True)
    ai_generated_content = models.TextField(blank=True, null=True)
 
    def __str__(self):
        return self.content
