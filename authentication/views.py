from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from authentication.serializers import BV_RegisterSerializer, RegisterSerializer
from media.models import ProfileImage
from user.models import BV_User, UserProfile
from user.serializers import BV_UserSerializer
from rest_framework import status

# Create your views here.

class RegisterView(generics.CreateAPIView):

    

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class BV_RegisterView(generics.CreateAPIView):
    
    def post(self, request,pk=None):
        ser = BV_RegisterSerializer(request.data)
        username             = ser.data['username']
        password             = ser.data['password']
        password2            = ser.data['password2']
        firstname            = ser.data['firstname']
        lastname             = ser.data['lastname']
        description          = ser.data['description']
        media_access_token   = ser.data['profile_image']


        #check if username is unique
        username_already_exists = UserProfile.username_already_exists(username=username)

        if ( username_already_exists):
            return Response({
            "error" : "User already exists"
            }, status=status.HTTP_409_CONFLICT)

        #check if password are identically
        if password != password2:
            return Response({
            "error" : "Passwords are not identically"
            }, status=status.HTTP_409_CONFLICT)

        #TODO: Check if passwords are difficult

        #create technical user
        user = User.objects.create_user(
            username=username, 
            password=password
        )

        #create user profile
        user_profile = UserProfile.objects.create(
            user                    = user,
            username                = username,
            description             = description,
            firstname               = firstname,
            lastname                = lastname,
            current_profile_image   = None
        )

        #get Profile Image with media_access_token
        profile_image = None

        if media_access_token != None:
            try:
                profile_image = ProfileImage.objects.get(media_access_token = media_access_token)
  
                profile_image.profile = user_profile
                
                user_profile.current_profile_image = profile_image

                profile_image.save()
                user_profile.save()

            except ProfileImage.DoesNotExist:
                td = "noting"

        #Select created userprofile
        profile = UserProfile.get_from_username(username)

        bv_user = BV_User.from_profile(profile)

        ser     = BV_UserSerializer(bv_user)

        return Response(ser.data, status=status.HTTP_201_CREATED)

