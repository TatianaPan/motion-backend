from django.contrib import admin

# Register your models here.

from app.users.models import UserProfile

admin.site.register(UserProfile)