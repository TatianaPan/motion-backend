from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

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
        blank=True
    )

    def __str__(self):
        return self.user.username

