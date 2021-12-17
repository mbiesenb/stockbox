from rest_framework import serializers
from core.serializers import TagSerializer
from media.models import BV_MediaUploadResponse, BV_PostMedia
from user.serializers import UserProfileSerializer

class BV_MediaUploadResponseSerializer(serializers.ModelSerializer):

    #upload_success = serializers.CharField(required=False, max_length=100)
    #uplo = serializers.CharField(required=False, )
    #message_text = serializers.CharField(required=False)
    #message_time = serializers.CharField(required=False)
    class Meta:
        model = BV_MediaUploadResponse
        fields = ("media_upload_key","media_access_token","upload_success","upload_message")
        depth = 1


class BV_PostMediaSerializer(serializers.ModelSerializer):

    media_access_token = serializers.CharField(required=True, max_length=100)

    class Meta:
       
        model = BV_PostMedia
        #fields = ("content_type", "media_access_token")
        fields = ("media_access_token",)
        depth = 1
    
    def create(validated_data):
        i = 3