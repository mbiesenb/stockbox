from rest_framework import serializers
from core.models import BV_ChatMessage, Tag, BV_Chat, BV_ChatMessageSend
from django.contrib.auth.password_validation import validate_password

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "text")

class BV_ChatSerializer(serializers.ModelSerializer):

    #receiver_username = serializers.CharField(required=False)
    #sender_image = serializers.CharField(required=False)
    #message_text = serializers.CharField(required=False)
    #message_time = serializers.CharField(required=False)
    class Meta:
        model = BV_Chat
        fields = ("partner_username","partner_profileImage", "latest_message_username", "latest_message_text", "latest_message_timestamp", "unread_message_count")

class BV_ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BV_ChatMessage
        fields = ("sender_username","receiver_username", "sender_image", "message_text","message_time")

class BV_ChatMessageSendSerializer(serializers.ModelSerializer):

    class Meta:
        model = BV_ChatMessageSend
        fields = ("message_text","receiver_username")

