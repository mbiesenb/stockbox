from django.db.models.fields import CharField
from rest_framework import serializers
from core.serializers import TagSerializer
from media.models import BV_PostMedia
from media.serializers import BV_MediaUploadResponseSerializer, BV_PostMediaSerializer
from user.serializers import UserProfileSerializer
from . models import BV_Comment, Comment, Snapshot, BV_Post, BV_MediaAccessToken



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text", "author")
        depth = 1


class SnapshotSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Snapshot
        fields = ("__all__")
        depth = 1

class BV_MediaAccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = BV_MediaAccessToken
        fields = ('media_access_token',)

class BV_PostSerializer(serializers.ModelSerializer):

    #profile = UserProfileSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    media = BV_PostMediaSerializer(many=True, read_only=True)

    #upvotes = serializers.IntegerField(required=False)
    #comment_count = serializers.IntegerField(required=False)
    #username =serializers.CharField(max_length=50, required=False)
    #tags = serializers.Li


    class Meta:
        model = BV_Post
        fields = ( "title", "description","upvotes", "comment_count", "username", "tags", "media")
        depth = 1



class BV_CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BV_Comment
        fields = ("username", "profileImagePreviewUrl", "comment_text", "upvotes")
        depth = 1
