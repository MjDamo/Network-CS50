# Generated by Django 5.0 on 2023-12-25 16:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_remove_post_likedby_post_likedby'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likedBy',
        ),
        migrations.AddField(
            model_name='post',
            name='likedBy',
            field=models.ManyToManyField(blank=True, related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]