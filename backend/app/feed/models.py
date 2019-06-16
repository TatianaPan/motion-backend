from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.


class Post(models.Model):
    title = models.CharField(
        verbose_name='post title',
        max_length=80,
        blank=True,
        null=True,
        default='Default title'
    )
    content = models.CharField(
        verbose_name='my post content',
        max_length=200,
        blank=True,
        null=True,
        default='Default post content'
    )
    created = models.DateField(
        verbose_name='created',
        auto_now_add=True,
        editable=False,
        blank=True
    )
    user = models.ForeignKey(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return self.content


class Like(models.Model):
    post = models.ForeignKey(
        verbose_name='post',
        to=Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
