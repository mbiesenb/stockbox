from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import IntegerField
from user.models import UserProfile



class Location(models.Model):
    longitude = models.CharField(max_length=8)
    latitude = models.CharField(max_length=8)
    locationText = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.longitude + "." + self.latitude + "->" + self.locationText


class MediaImage(models.Model):
    img_x = models.IntegerField()
    img_y = models.IntegerField()

    def __str__(self) -> str:
        return "image"


class MediaVideo(models.Model):
    duration = models.IntegerField()

    def __str__(self) -> str:
        return "video"


class SnapShotMedia(models.Model):
    media_type = models.IntegerField()
    media_url = models.CharField(max_length=50, default='')
    media_filetype = models.CharField(max_length=50)
    media_image = models.ForeignKey(
        MediaImage, on_delete=models.SET_NULL, related_name='media_image', null=True)
    media_video = models.ForeignKey(
        MediaVideo, on_delete=models.SET_NULL, related_name='media_video', null=True)

    def __str__(self) -> str:
        return self.type

# @dataclass


class BV_Post(models.Model):
    media_type = ""
    media_url = ""
    snapshot = None
    upvotes = 0
    comment_count = 0
    profile = None
    tags = list()

    def __init__(self, psnapshot, upvotes, comment_count, profile, tags, media_type, media_url):
        self.media_type = media_type
        self.media_url = media_url
        self.snapshot = psnapshot
        self.upvotes = upvotes
        self.comment_count = comment_count
        self.profile = profile
        self.tags = tags

    class Meta:
        managed = False


class Snapshot(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    author = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, related_name='snapshots', null=True)
    media = models.ForeignKey(
        SnapShotMedia, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True)
    upvotes = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=200)
    snapshot = models.ForeignKey(
        Snapshot, related_name='comments', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True)
    upvotes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.text

    #def get(username):

#+ UserProfile
#    + Username
#    + ProfileImage
#+ Kommentar
#    + Kommentartext
#    + Upvotes
#    + Anzahl Sub-Kommentare

class BV_Comment(models.Model):
    username = ""
    profileImagePreviewUrl = ""
    comment_text = ""
    upvotes = 0

    def __init__(self, username, profileImagePreviewUrl, comment_text, upvotes):
        self.username = username
        self.profileImagePreviewUrl = profileImagePreviewUrl
        self.comment_text = comment_text
        self.upvotes = upvotes

        class Meta:
            managed = False

