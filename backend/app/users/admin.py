from django.contrib import admin

# Register your models here.

from app.users.models import *

admin.site.register(UserProfile)
admin.site.register(Follower)
admin.site.register(Friend)
