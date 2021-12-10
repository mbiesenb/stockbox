from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import IntegerField
import media
from user.models import UserProfile



class Location(models.Model):
    longitude = models.CharField(max_length=8)
    latitude = models.CharField(max_length=8)
    locationText = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.longitude + "." + self.latitude + "->" + self.locationText

class BV_MediaAccessToken(models.Model):
    
    media_access_token = ""

    def __init(self, media_access_token):
        self.media_access_token = media_access_token

class BV_Post(models.Model):
    title           = ""
    description     = ""
    snapshot        = None
    upvotes         = 0
    comment_count   = 0
    username        = ""
    media           = list()
    tags            = list()

    def __init__(self, title, description, psnapshot, upvotes, comment_count, username, tags, media):
        self.title = title
        self.description = description
        self.snapshot = psnapshot
        self.upvotes = upvotes
        self.comment_count = comment_count
        self.username = username
        self.tags = tags
        self.media = media.all()

    class Meta:
        managed = False

    def from_snapshot(snapshot):
        upvotes         = snapshot.snapshot_upvotes.count()
        comment_count   = snapshot.comments.count()
        username        = snapshot.author.username
        tags            = snapshot.tags
        title           = snapshot.title
        description     = snapshot.description
        media           = snapshot.media   

        bv_post = BV_Post(
            psnapshot       = snapshot,
            comment_count   = comment_count,
            username        = username,
            tags            = tags,
            upvotes         = upvotes,
            title           = title,
            description     = description,
            media           = media #TODO: Fix this

        )

        return bv_post


class Snapshot(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    author = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, related_name='snapshots', null=True)
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

