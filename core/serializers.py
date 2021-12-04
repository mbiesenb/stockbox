from rest_framework import serializers
from core.models import Comment, Snapshot, UserProfile, Tag
from django.contrib.auth import get_user_model 
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "text")



