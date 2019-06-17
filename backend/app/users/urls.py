from django.urls import path

from app.users.views import *

urlpatterns = [
    path('', GetAllUsers.as_view(), name='get-all-users'),
    path('search', SearchUsers.as_view()),
    path('<int:user_id>/', GetUserProfile.as_view())

]