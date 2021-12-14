from django.contrib import admin
from post.models import Snapshot, Comment
from core.models import Tag
from user.models import UserProfile
from media.models import ProfileImage
from post.models import Location


# Register your models here.
admin.site.register(Snapshot)
admin.site.register(UserProfile)
admin.site.register(ProfileImage)
admin.site.register(Location)
admin.site.register(Comment)
admin.site.register(Tag)

