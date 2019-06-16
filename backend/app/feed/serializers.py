from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.feed.models import Post, Like
from users.serializers import UserSerializer

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user']


class PostForPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'user']


class LikeSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ['post']


class LikeForPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

