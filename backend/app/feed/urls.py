from django.contrib import admin
from django.urls import path

from app.feed.views import *

urlpatterns = [
    path('', GetAllPosts.as_view(), name='get-all-posts'),
    path('posts/<int:post_id>/', GetUpdateDeleteSpecificPost.as_view(), name='get-post'),
    path('posts/new-post/', CreatePost.as_view(), name='create-new-post'),
    path('<int:user_id>/', GetAllPostsOfUser.as_view()),
    path('posts/likes/', GetLikedPosts.as_view()),
    path('posts/like/<int:post_id>/', LikePost.as_view()),
    path('sr', SearchPosts.as_view()),
    path('posts/like/<int:post_id>/', UnlikePost.as_view()),
    path('posts/share-post/<int:post_id>/', ShareAPost.as_view())

]
