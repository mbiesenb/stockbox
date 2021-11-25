from django.contrib import admin
from django.db import models
from . models import Snapshot , UserProfile , UserImage , Location ,  Comment , Tag


# Register your models here.
admin.site.register(Snapshot)
admin.site.register(UserProfile)
admin.site.register(UserImage)
admin.site.register(Location)
admin.site.register(Comment)
admin.site.register(Tag)

