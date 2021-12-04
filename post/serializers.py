from rest_framework import serializers
from core.serializers import TagSerializer
from user.serializers import UserProfileSerializer
from . models import Comment, Snapshot, BV_Post



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

class BV_PostSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BV_Post
        fields = ("media_type", "media_url", "upvotes",
                  "comment_count", "profile", "tags")
        depth = 1
