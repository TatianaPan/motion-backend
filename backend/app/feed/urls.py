from django.contrib import admin
from django.urls import path

from app.feed.views import GetPostsView

urlpatterns = [
    path('', GetPostsView.as_view(), name='get-all-posts'),
    # path('<int:post_id>/', GetPostView.as_view(), name='get-post')

]
