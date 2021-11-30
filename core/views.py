from django.db.models.query import QuerySet
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
from . models import Snapshot, Tag, UserProfile, BV_Post
from . serializers import SnapshotSerializer, UserProfileSerializer, RegisterSerializer,  BV_PostSerializer
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


# Create your views here.
# http://www.tomchristie.com/rest-framework-2-docs/api-guide/routers


class SnapShotViewSet(viewsets.ModelViewSet):

    #permission_classes = (IsAuthenticated,)
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer

    def list(self, request):
        ser = SnapshotSerializer(self.queryset, many=True)
        return Response(ser.data, status.HTTP_200_OK)

    def create(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        snapshot = get_object_or_404(self.queryset, pk=pk)
        ser = SnapshotSerializer(snapshot)
        return Response(ser.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        snapshot = get_object_or_404(self.queryset, pk=pk)
        snapshot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    #permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
#mixins.ListModelMixin,  viewsets.GenericViewSet

class BV_PostView(generics.CreateAPIView):

    serializer_class = BV_PostSerializer
    #queryset = Snapshot.objects.all()
    
    def get(self, request,pk=None):


        bv_post = BV_Post()

        snapshot = get_object_or_404(Snapshot.objects.all(), pk=1)

        #bv_post.snapshot = get_object_or_404(queryset, pk=1)
        #bv_post.upvotes = snapshot.prefetch_related('snapshot_upvotes').count()
        bv_post.upvotes = snapshot.snapshot_upvotes.count()
        bv_post.comment_count = snapshot.comments.count()
        bv_post.profile = snapshot.author
        bv_post.tags = snapshot.tags
        
        ser = BV_PostSerializer(data=bv_post)
        ser.is_valid(raise_exception=True)
        return Response(ser.data)
