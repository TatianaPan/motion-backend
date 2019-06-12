from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views import View
import json
from app.feed.models import Post

User = get_user_model()


class GetPostsView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.values('content').all()
        posts = list(posts)
        return JsonResponse(posts, safe=False)

