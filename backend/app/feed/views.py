from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.views import View
import json

from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import request, generics, filters, status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from app.feed.models import Post, Like
from app.feed.serializers import PostSerializer, PostForPostingSerializer, LikeSerializer, LikeForPostSerializer
from app.feed.permissions import IsOwnerOrReadOnly
from app.users.models import Follower

User = get_user_model()


class GetAllPosts(ListAPIView):
    """
    GET: lists all the posts of all users in chronological order
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class GetAllPostsOfUser(ListAPIView):
    """
    GET: lists all the posts of a specific user in chronological order
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.queryset.filter(user__id=self.kwargs.get('user_id'))


class CreatePost(CreateAPIView):
    """
    POST: logged-in user or admin can make a new post by sending post data
    """
    permission_classes = (IsAuthenticated & IsOwnerOrReadOnly | IsAuthenticated & IsAdminUser,)
    queryset = Post.objects.all()
    serializer_class = PostForPostingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetUpdateDeleteSpecificPost(RetrieveUpdateDestroyAPIView):
    """
    RETRIEVE: get a specific post by ID and display all the information
    PATCH: update a specific post (only by owner of post or admin)
    DELETE: delete a post by ID (only by owner of post or admin)
    """
    permission_classes = (IsAuthenticated & IsOwnerOrReadOnly | IsAuthenticated & IsAdminUser,)
    queryset = Post.objects.all()
    serializer_class = PostForPostingSerializer
    lookup_url_kwarg = 'post_id'


class GetLikedPosts(ListAPIView):
    """
    GET: the list of the posts the current user likes
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.queryset.filter(likes__user=self.request.user.id)


class GetFollowedPosts(ListAPIView):
    """
    GET: lists all the posts of followed users in chronological order
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        new_list = self.queryset.filter(user__followees__follower=self.request.user.id)
        return new_list.order_by('-created')


class CreateDeleteLike(APIView):
    """
    POST: like a post
    DELETE: remove like from a post
    """

    queryset = Like.objects.all()
    serializer_class = LikeForPostSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, id=kwargs.get('post_id'))
        like = Like(user=user, post=post)
        like.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        post = kwargs["post_id"]
        user = request.user.id
        Like.objects.get(post=post, user=user).delete()
        return Response("delete successful")

# class LikePost(CreateAPIView):
#     """
#     POST: like a post
#     """
#
#     queryset = Like.objects.all()
#     serializer_class = LikeForPostSerializer
#
#     def create(self, request, *args, **kwargs):
#         user = self.request.user
#         post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
#         like = Like(user=user, post=post)
#         like.save()
#         return Response(status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
    #     serializer.save(user=self.request.user, post=post)


# class UnlikePost(DestroyAPIView, GenericAPIView):
#     """
#     DELETE: remove like from a post
#     """
#     #permission_classes = (IsAuthenticated & IsOwnerOrReadOnly,)
#
#     queryset = Like.objects.all()
#     serializer_class = LikeForPostSerializer
#
#     def delete(self, request, *args, **kwargs):
#         post = self.kwargs["post_id"]
#         user = self.request.user.id
#         Like.objects.get(post=post, user=user).delete()
#         return Response("delete successful")


    # def perform_destroy(self, instance):
    #     post = self.kwargs.get('post_id')
    #     instance.delete(post=post, user=self.request.user)


# class SearchPosts(ListAPIView):
#     """
#     GET: Search posts of all users and list result in chronological order
#     """
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter(content=self.kwargs.get('search_string'))


class SearchPosts(ListAPIView):
    """
    GET: Search posts of all users and list result in chronological order
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('content',)


class ShareAPost(CreateAPIView):
    pass


