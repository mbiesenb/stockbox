from rest_framework import serializers
from . models import Comment, Snapshot, UserProfile, Tag, BV_Post
from django.contrib.auth import get_user_model 
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('firstname', 'lastname', 'user')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "text")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text","author")
        depth = 1


class SnapshotSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Snapshot
        fields = ("__all__")
        depth = 1


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
    
        user.set_password(validated_data['password'])
        user.save()

        return user

class BV_PostSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BV_Post
        fields = ("upvotes","comment_count","profile","tags")
        depth = 1