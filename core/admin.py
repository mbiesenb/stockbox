from django.contrib import admin
from django.db import models
from . models import Snapshot , UserProfile , Comment , Tag
from user.models import UserImage
from post.models import Location


# Register your models here.
admin.site.register(Snapshot)
admin.site.register(UserProfile)
admin.site.register(UserImage)
admin.site.register(Location)
admin.site.register(Comment)
admin.site.register(Tag)

