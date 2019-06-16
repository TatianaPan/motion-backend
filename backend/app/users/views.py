from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework import request, filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from users.serializers import UserSerializer

User = get_user_model()


class GetAllUsers(ListAPIView):
    """
    GET: Get all the users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SearchUsers(ListAPIView):
    """
    GET: Search users
    in Postman add in Params key: search, value: string
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class GetUserProfile(RetrieveAPIView):
    """
    GET: Get specific user profile
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'

