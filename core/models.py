from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
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
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    pic = models.ForeignKey(UserImage, on_delete=models.SET_NULL, null=True)
    def __str__(self) -> str:
        return self.nick


class SnapShotImage(models.Model):
    filename = models.CharField(max_length=50)
    filetype = models.CharField(max_length=10)
    img_x = models.IntegerField()
    img_y = models.IntegerField() 
    #pic = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self) -> str:
        return self.filename + "." + self.filetype


class Location(models.Model):
    longitude = models.CharField(max_length=8)
    latitude = models.CharField(max_length=8)
    locationText = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.longitude + "." + self.latitude + "->" + self.locationText


class Snapshot(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    pic = models.ForeignKey(SnapShotImage, on_delete=models.SET_NULL, null=True)
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