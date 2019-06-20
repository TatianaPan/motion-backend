from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    hobby = models.CharField(
        verbose_name='hobby',
        max_length=200,
        blank=True
    )
    age = models.IntegerField(
        verbose_name='age',
        blank=True,
        null=True
    )
    validation = models.CharField(
        verbose_name='code',
        max_length=32,
        blank=True
    )

    def __str__(self):
        return self.user.username


class Follower(models.Model):
    follower = models.ForeignKey(
        verbose_name='follower',
        to=User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    followed_by = models.ForeignKey(
        verbose_name='follower',
        to=User,
        on_delete=models.CASCADE,
        related_name='followees'
    )

    def __str__(self):
        return self.follower.username


class Friend(models.Model):
    status = models.CharField(
        verbose_name='status',
        max_length=50,
        blank=True
    )
    created = models.DateField(
        verbose_name='created',
        auto_now_add=True,
        editable=False,
        blank=True
    )
    receiver = models.ForeignKey(
        verbose_name='receiver',
        to=User,
        on_delete=models.CASCADE,
        related_name='received'
    )
    requester = models.ForeignKey(
        verbose_name='requester',
        to=User,
        on_delete=models.CASCADE,
        related_name='requested'
    )
