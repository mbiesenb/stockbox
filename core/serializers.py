from rest_framework import serializers
from core.models import BV_ChatMessage, Tag, BV_Chat
from django.contrib.auth.password_validation import validate_password

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "text")

class BV_ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BV_Chat
        fields = ("partner_username","partner_profileImage", "latest_message_username", "latest_message_text", "latest_message_timestamp", "unread_message_count")

class BV_ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BV_ChatMessage
        fields = ("username", "sender_image", "me", "message_text","message_time")

