from rest_framework import serializers
from . models import BV_User
from core.serializers import BV_PostSerializer


    username = ""
    userDescription = ""
    followers_count = 0
    following_count  = 0
    posts = list()


class BV_UserSerializer(serializers.ModelSerializer):

    posts = BV_PostSerializer(many=True, read_only=True)

    class Meta:
        model = BV_User
        fields = ("username","userDescription","followers_count","following_count","posts")
        depth = 1