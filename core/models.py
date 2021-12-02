from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import IntegerField
from dataclasses import dataclass
from typing import List
#from django.db.models.base import Model


# Create your models here.

class UserImage(models.Model):
    filename = models.CharField(max_length=50)
    filetype = models.CharField(max_length=10)
    img_x = models.IntegerField()
    img_y = models.IntegerField() 
    #pic = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self) -> str:
        return self.filename + "." + self.filetype


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='profile')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    pic = models.ForeignKey(UserImage, on_delete=models.SET_NULL, null=True)
    def __str__(self) -> str:
        return self.user





class Location(models.Model):
    longitude = models.CharField(max_length=8)
    latitude = models.CharField(max_length=8)
    locationText = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.longitude + "." + self.latitude + "->" + self.locationText

class MediaImage(models.Model):
    img_x = models.IntegerField()
    img_y = models.IntegerField() 
    #pic = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self) -> str:
        return "image"

class MediaVideo(models.Model):
    duration = models.IntegerField()
    #pic = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self) -> str:
        return "video"


class SnapShotMedia(models.Model):
    media_type = models.IntegerField()
    media_url = models.CharField(max_length=50)
    media_filetype = models.CharField(max_length=50)
    media_image = models.ForeignKey(MediaImage, on_delete=models.SET_NULL,related_name='media_image', null=True)
    media_video = models.ForeignKey(MediaVideo, on_delete=models.SET_NULL, related_name='media_video', null=True)

    def __str__(self) -> str:
        return self.type

class Snapshot(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    media = models.ForeignKey(SnapShotMedia, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    upvotes = models.IntegerField()


    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=200) 
    snapshot = models.ForeignKey(Snapshot, related_name='comments',on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True) 
    upvotes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.text


class Tag(models.Model):
    text = models.CharField(max_length=30)
    snapshot = models.ForeignKey(Snapshot, related_name='tags', on_delete=models.SET_NULL, null=True) 
    author = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.text

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='sender' ,null=True)
    receiver = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='receiver',null=True)
    text = models.CharField(max_length=500)

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='follower',null=True)
    stalker = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='stalker',null=True)

class Upvote(models.Model):
    upvoter = models.ForeignKey(UserProfile, on_delete=SET_NULL, related_name='upvoter', null=True)
    type = models.IntegerField() #1 = tag, 2=comment, 3 = snapshot
    tag = models.ForeignKey(Tag, on_delete=SET_NULL, related_name='tag_upvotes', null=True)
    comment = models.ForeignKey(Comment, on_delete=SET_NULL, related_name='comment_upvotes', null=True)
    snapshot = models.ForeignKey(Snapshot, on_delete=SET_NULL, related_name='snapshot_upvotes', null=True)

#@dataclass
class BV_Post(models.Model):
    media_type = ""
    media_url = ""
    snapshot = None
    upvotes  = 0
    comment_count = 0
    profile  = None
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