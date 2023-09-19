# Generated by Django 4.1.2 on 2023-08-16 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0007_reply_dislikes_reply_likes_alter_reply_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='retweets',
            field=models.ManyToManyField(blank=True, related_name='retweeted_replies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reply',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_replies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reply',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_replies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reply',
            name='tweet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='tweets.tweet'),
        ),
    ]
