from django.contrib import admin

# Register your models here.

from app.feed.models import Post, Like

admin.site.register(Post)
admin.site.register(Like)
