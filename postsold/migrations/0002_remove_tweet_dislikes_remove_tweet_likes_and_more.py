# Generated by Django 4.1.2 on 2023-08-12 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='tweet',
            name='retweets',
        ),
        migrations.AddField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
