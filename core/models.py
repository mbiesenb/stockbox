from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import IntegerField
from post.models import Snapshot, Comment
from user.models import UserProfile
# Create your models here.


class Tag(models.Model):
    text        = models.CharField(max_length=30)
    snapshot    = models.ForeignKey(Snapshot, related_name='tags', on_delete=models.SET_NULL, null=True) 
    author      = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.text

class Message(models.Model):
    sender      = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='sender' ,null=True)
    receiver    = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='receiver',null=True)
    text        = models.CharField(max_length=500)

class Follow(models.Model):
    follower    = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='following',null=True)
    stalker     = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='followers',null=True)

class Upvote(models.Model):
    upvoter     = models.ForeignKey(UserProfile, on_delete=SET_NULL, related_name='upvoter', null=True)
    type        = models.IntegerField() #1 = tag, 2=comment, 3 = snapshot
    tag         = models.ForeignKey(Tag, on_delete=SET_NULL, related_name='tag_upvotes', null=True)
    comment     = models.ForeignKey(Comment, on_delete=SET_NULL, related_name='comment_upvotes', null=True)
    snapshot    = models.ForeignKey(Snapshot, on_delete=SET_NULL, related_name='snapshot_upvotes', null=True)


