from django.shortcuts import render
from . models import BV_User, BV_UserPostPreview
from core.models import UserProfile #NEEDS TO BE CHANGED
from . serializers import BV_UserSerializer, BV_UserPostsPreviewSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from core.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


# I NEED TO CREATE A BV_UPLOAD

class BV_UserView(generics.CreateAPIView):

    serializer_class = BV_UserSerializer
    

    def get(self, request,username='user1'):
        user =            get_object_or_404(User, username=username)
        userProfile     = UserProfile.get( user.username )
        username        = userProfile.username
        profile_image   = "empty"
        userDescription = userProfile.description
        followers_count = userProfile.followers.count()
        following_count = userProfile.following.count()

        snapshots       = userProfile.snapshots.all()

        posts            = BV_UserPostPreview.get_from_snapshots(snapshots)

        bv_post = BV_User(
            username        =username,
            profile_image   =profile_image,
            userDescription =userDescription,
            followers_count =followers_count,
            following_count =following_count,
            posts = posts
        )
        ser = BV_UserSerializer(bv_post)

        #ser.is_valid(raise_exception=True)

        return Response(ser.data)

