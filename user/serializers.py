from rest_framework import serializers
from . models import BV_User, BV_UserPostPreview
#from core.serializers import BV_PostSerializer


class BV_UserPostsPreviewSerializer(serializers.ModelSerializer):

    class Meta:
        model =  BV_UserPostPreview
        fields = ("description","previewUrl")

class BV_UserSerializer(serializers.ModelSerializer):

    posts = BV_UserPostsPreviewSerializer(many=True, read_only=True)

    class Meta:
        model = BV_User
        fields = ("username","profile_image","userDescription","followers_count","following_count","posts")
        depth = 1