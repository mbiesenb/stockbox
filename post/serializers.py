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
    tags = TagSerializer(many=True, required=False)
    media = BV_PostMediaSerializer(many=True, required=False)

    title = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=100, required=False)
    upvotes = serializers.IntegerField(required=False)
    comment_count = serializers.IntegerField(required=False)
    username =serializers.CharField(max_length=100, required=False)

    #def create(self, validated_data):
    #    choice_validated_data = validated_data.pop('choice_set')
    #    question = 1 #Question.objects.create(**validated_data)
    #    choice_set_serializer = self.fields['choice_set']
    #    for each in choice_validated_data:
    #        each['question'] = question
    #    choices = choice_set_serializer.create(choice_validated_data)
    #    return question

    #def __init__(self, *args, **kwargs):
    #    self.media = BV_PostMediaSerializer(data= args[0].media, many=True)
    class Meta:
        model = BV_Post
        fields = ( "title", "description","upvotes", "comment_count", "username", "tags", "media")
        depth = 2



class BV_CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BV_Comment
        fields = ("username", "profileImagePreviewUrl", "comment_text", "upvotes")
        depth = 1
