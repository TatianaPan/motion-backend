from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from app.users.models import UserProfile, Follower, Friend

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserProfileSerializer(serializers.ModelSerializer):
    # user = FullUserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'hobby', 'age', 'validation']
        extra_kwargs = {
            'validation': {
                # write only (cant be read afterwards)
                'write_only': True
            }
        }


class FullUserSerializer(WritableNestedModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     # Unless the application properly enforces that this field is
    #     # always set, the follow could raise a `DoesNotExist`, which
    #     # would need to be handled.
    #     profile = instance.user
    #
    #     instance.hobby = validated_data.get('hobby', instance.username)
    #     instance.age = validated_data.get('age', instance.email)
    #     instance.save()
    #     profile.is_premium_member = user_data.get(
    #         'is_premium_member',
    #         profile.is_premium_member
    #     )
    #     profile.has_support_contract = user_data.get(
    #         'has_support_contract',
    #         profile.has_support_contract
    #     )
    #     profile.save()
    #
    #     return instance


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer()
    followed_by = UserSerializer()

    class Meta:
        model = Follower
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    requester = UserSerializer()

    class Meta:
        model = Friend
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class RegistrationValidationSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
