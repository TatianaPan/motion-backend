from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework import request, filters
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, filters, status
from django.contrib.auth.hashers import make_password

from app.users.models import UserProfile, Follower, Friend
from app.feed.permissions import IsOwnerOrReadOnly
from app.users.serializers import *
from django.utils.crypto import get_random_string

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
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    lookup_url_kwarg = 'user_id'

    lookup_field = 'user_id'

    # def get_queryset(self):
    #     user_id = User.objects.get(id=self.kwargs.get('pk'))
    #     return self.queryset.filter(user_id=user_id.id)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     user_id = User.objects.get(id=self.kwargs.get('user_id'))
    #     print(user_id)
    #     instance = self.get_object(self.queryset)
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


class FollowAUser(CreateAPIView):
    """
    POST: follow a user
    Send an email to the user if they get followed by someone
    """

    queryset = Follower.objects.all()
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        follower = self.request.user
        followed_by = get_object_or_404(User, id=self.kwargs.get('user_id'))
        new_followee = Follower(follower=follower, followed_by=followed_by)
        new_followee.save()
        send_mail(
            'Subject here',
            f'You are followed by {follower}',
            'students@propulsionacademy.com',
            [followed_by.email],
            fail_silently=False,
        )
        return Response(status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
    #     serializer.save(user=self.request.user, post=post)


class UnfollowAUser(DestroyAPIView):
    """
    DELETE: unfollow a user
    """
    permission_classes = (IsAuthenticated & IsOwnerOrReadOnly,)
    queryset = Follower.objects.all()
    serializer_class = FollowSerializer
    # lookup_field = 'followed_by'
    # lookup_url_kwarg = 'user_id'

    def delete(self, request, *args, **kwargs):
        followed_by = self.kwargs['user_id']
        follower = self.request.user.id
        Follower.objects.get(followed_by=followed_by, follower=follower).delete()
        return Response("You do not follow this user")

    # def perform_destroy(self, instance):
    #     followed_by = get_object_or_404(User, id=self.kwargs.get('user_id'))
    #     instance.delete(followed_by=followed_by, follower=self.request.user)


class GetListOfFollowers(ListAPIView):
    """
    GET: List of all the logged in user’s followers
    """
    permission_classes = (IsAuthenticated,)
    queryset = Follower.objects.all()
    serializer_class = FollowSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        followers = user.followees.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)


class GetFollowedByUser(ListAPIView):
    """
    GET: List of all the people the user is following
    """
    permission_classes = (IsAuthenticated,)
    queryset = Follower.objects.all()
    serializer_class = FollowSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        followed_by = user.followers.all()
        serializer = self.get_serializer(followed_by, many=True)
        return Response(serializer.data)


class GetUpdateProfile(RetrieveUpdateAPIView):
    """
    GET: Get logged in user’s profile (as well private information like email, etc.)
    PATCH: Update the logged in user’s profile public info
    """
    permission_classes = (IsAuthenticated & IsOwnerOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = FullUserSerializer

    # def get_queryset(self, request, *args, **kwargs):
    #     self.kwargs['pk'] = self.request.user
    #     return self.queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # me = user.profile
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        self.kwargs['pk'] = self.request.user
        # user = self.request.user
        #me = user.profile
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # def patch(self, request):
    #     user_profile =

    # def partial_update(self, request, *args, **kwargs):
    #     #partial = kwargs.pop('partial', False)
    #     kwargs['partial'] = True
    #     user = self.request.user
    #     #me = user.profile
    #     serializer = self.get_serializer(user, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class SendFriendRequest(CreateAPIView):
    """
    POST: Send friend request to another user
    Send an email to the user if they get a friend request
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def create(self, request, *args, **kwargs):
        requester = request.user
        receiver = get_object_or_404(User, id=kwargs.get('user_id'))
        friend_request = Friend(requester=requester, receiver=receiver, status='pending')
        friend_request.save()
        send_mail(
            'Subject here',
            f'You got a new friend request from {requester}',
            'students@propulsionacademy.com',
            [receiver.email],
            fail_silently=False,
        )
        return Response(status=status.HTTP_201_CREATED)


class ListOpenRequests(ListAPIView):
    """
     GET: List all open friend requests from others
    """
    # permission_classes = (IsAuthenticated & IsOwnerOrReadOnly,)
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def get_queryset(self):

        open_requests = self.queryset.filter(status='pending', receiver=self.request.user.id)
        return open_requests


class GetPendingRequests(ListAPIView):
    """
    GET: List all the logged in user’s pending friend requests
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def get_queryset(self):
        pending_requests = self.queryset.filter(requester=self.request.user.id, status='pending')
        return pending_requests


# /api/users/friendrequests/accept/<int:request_id>/

class AcceptFriendRequest(UpdateAPIView):
    """
     PATCH: Accept an open friend request
     Send an email if a friend request gets accepted
    """
    # permission_classes = (IsAuthenticated & IsOwnerOrReadOnly,)
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    lookup_url_kwarg = 'request_id'

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        receiver = request.user
        requester = get_object_or_404(Friend, id=kwargs.get('request_id'))
        user = get_object_or_404(User, requested=requester)
        send_mail(
            'Subject here',
            f'Your friend request has been accepted by {receiver}',
            'students@propulsionacademy.com',
            [user.email],
            fail_silently=False,
        )
        return self.update(request, *args, **kwargs)


# /api/users/friendrequests/reject/<int:request_id>/
class RejectFriendRequest(UpdateAPIView):
    """
    PATCH: Reject an open friend request
    """
    # permission_classes = (IsAuthenticated & IsOwnerOrReadOnly,)
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    lookup_url_kwarg = 'request_id'


# /api/users/friends/
class ListAcceptedFriends(ListAPIView):
    """
     GET: List all accepted friends
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def get_queryset(self):
        friends = self.queryset.filter(receiver=self.request.user.id, status='accepted')
        return friends


# /api/users/friends/unfriend/<int:user_id>/
class UnfriendUser(DestroyAPIView):
    """
    DELETE: Unfriend a user
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def delete(self, request, *args, **kwargs):
        requester = kwargs["user_id"]
        receiver = request.user.id
        Friend.objects.get(status='accepted', receiver=receiver, requester=requester).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# /api/registration/
class RegistrationView(GenericAPIView):
    """
    POST: Register a new user by asking for an email (send email validation code)
    """
    permission_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = request.data['email']
        validation_code = get_random_string(length=32)
        new_user = User.objects.create(password=validation_code, email=user_email)
        new_user.save()
        send_mail(
            'Registration at Propulsion',
            f'Your validation code is: {validation_code}',
            'students@propulsionacademy.com',
            [new_user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(self.get_serializer(new_user).data)


# /api/registration/validation/
class RegistrationValidationView(GenericAPIView):
    """
    POST: Validate a new registered user with a validation code sent by email
    """
    permission_classes = []
    serializer_class = RegistrationValidationSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data['username']
        validation_code = request.data['code']
        email = request.data['email']
        password = request.data['password']

        new_user = User.objects.get(email=email)

        if new_user.password == validation_code:
            new_user.username = username
            new_user.password = make_password(password)
            new_user.save()
        else:
            return Response('Incorrect validation code', status=400)

        return Response('New user has been successfully created', status=201)

        # try:
        #     new_user = get_object_or_404(User, email=request.data)
        #     if new_user.validation == request.data.validation:
        #         pass
        #     validation = get_object_or_404(UserProfile, validation=request.data)
        # except User.DoesNotExist:
        #     return Response('User with this email or validation code does not exist', status=400)
        #
        # user = User(email=email, username=username, password=password)
        # user.save()
        # #
        # if email == User.objects.get(email=request.data) and validation == UserProfile.objects.get(validation=validation):
        #     user = serializer.save(username=username, password=password)
        #
        # else:
        #     return Response('User with this email or validation code does not exist', status=400)

        # email = get_object_or_404(User, email=request.data)
        # validation = get_object_or_404(UserProfile, validation=request.data)
        # user = serializer.save(
        #     serializer.validated_data,
        # )

    # try:
        #     email = User.objects.get(email=self.request.data)
        #     user = User.objects.get(id=post_dict['user'])
        # except User.DoesNotExist:
        #     return Response('User with this email or validation code does not exist', status=400)

        # try:
        #     validation_code = UserProfile.objects.get(user__id__)

