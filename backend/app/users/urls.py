from django.urls import path

from app.users.views import *

urlpatterns = [
    path('', GetAllUsers.as_view(), name='get-all-users'),
    path('search', SearchUsers.as_view()),
    path('<int:user_id>/', GetUserProfile.as_view()),
    path('follow/<int:user_id>/', FollowAUser.as_view()),
    path('unfollow/<int:user_id>/', UnfollowAUser.as_view()),
    path('followers/', GetListOfFollowers.as_view()),
    path('following/', GetFollowedByUser.as_view()),
    path('me/', GetUpdateProfile.as_view()),
    path('friendrequests/<int:user_id>/', SendFriendRequest.as_view()),
    path('friendrequests/', ListOpenRequests.as_view()),
    path('friendrequests/pending/', GetPendingRequests.as_view()),
    path('friendrequests/accept/<int:request_id>/', AcceptFriendRequest.as_view()),
    path('friendrequests/reject/<int:request_id>/', RejectFriendRequest.as_view()),
    path('friends/', ListAcceptedFriends.as_view()),
    path('friends/unfriend/<int:user_id>/', UnfriendUser.as_view()),
    path('registration/', RegistrationView.as_view()),
    path('registration/validation/', RegistrationValidationView.as_view())

]
