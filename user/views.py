from django.shortcuts import render
from . models import BV_User
from core.models import UserProfile #NEEDS TO BE CHANGED
from . serializers import BV_UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# I NEED TO CREATE A BV_UPLOAD

class BV_UserView(generics.CreateAPIView):

    serializer_class = BV_UserSerializer
    
    #("username","userDescription","followers_count","following_count","posts")

    def get(self, request,pk=None):
        user =        get_object_or_404(User.objects.all(), pk=pk)
        userProfile     = user.profile

        username        = userProfile.username
        userDescription = userProfile.description
        followers_count = userProfile.followers.count()
        following_count = userProfile.following.count()
        post            = None # TBD

        bv_post = BV_User(
            username=username,
            comment_count=comment_count,
            profile=profile,
            tags=tags,
            upvotes=upvotes,
            media_url = media_url,
            media_type = media_type
        )
        #dict_obj = model_to_dict( tags )
        #serialized = json.dumps(dict_obj)
        #print(serialized)
        ser = BV_PostSerializer(bv_post)
        #ser.is_valid(raise_exception=True)
        return Response(ser.data)

# Create your views here.
