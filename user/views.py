from django.shortcuts import render
from . models import BV_User, BV_UserPostPreview
from core.models import UserProfile #NEEDS TO BE CHANGED
from . serializers import BV_UserSerializer, BV_UserPostsPreviewSerializer, UserProfileSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from core.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status


# I NEED TO CREATE A BV_UPLOAD

class BV_UserView(generics.CreateAPIView):

    serializer_class = BV_UserSerializer
    

    def get(self, request,username):
        user    = get_object_or_404(User, username=username)
        profile = UserProfile.get( user.username )
        bv_post = BV_User.from_profile(profile)
        ser     = BV_UserSerializer(bv_post)
        return Response(ser.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request):
        ser = UserProfileSerializer(self.queryset, many=True)
        return Response(ser.data, status.HTTP_200_OK)

    def create(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        snapshot = get_object_or_404(self.queryset, pk=pk)
        ser = UserProfileSerializer(snapshot)
        return Response(ser.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        snapshot = get_object_or_404(self.queryset, pk=pk)
        snapshot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

