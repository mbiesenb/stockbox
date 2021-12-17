from django.core.exceptions import ValidationError
from django.shortcuts import render
from media.models import BV_MediaUploadResponse, SnapShotMedia
from media.serializers import BV_MediaUploadResponseSerializer
from post.models import BV_Post, Comment, Snapshot, BV_Comment
from post.serializers import SnapshotSerializer, BV_PostSerializer, BV_CommentSerializer
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from user.models import UserProfile
from django.forms.models import model_to_dict

# Create your views here.

class SnapShotViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

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


class BV_CommentView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = BV_CommentSerializer
    queryset = Snapshot.objects.all()

    def get(self, request, pk=None):

        bv_comments = list()
        snapshot = get_object_or_404( self.queryset , pk=pk)

        comments = snapshot.comments.all()

        bv_comments = list()
        # TODO
        for comment in comments:
            
            bv_comment = BV_Comment.from_comment(comment=comment)

            bv_comments.append(bv_comment)

        ser = BV_CommentSerializer(bv_comments, many=True) 
        #ser.is_valid(raise_exception=True)
        return Response(ser.data)
    
    def post(self, request, pk=None):

        snapshot = get_object_or_404( self.queryset , pk=pk)

        bv_comment = BV_CommentSerializer(request.data)

        comment_text = bv_comment.data['comment_text']

        profile_me = UserProfile.get_from_username(request.user.username)

        comment = Comment.objects.create(
            text        = comment_text,
            snapshot    = snapshot,
            author      = profile_me,
            upvotes     = 0
        )

        bv_comment = BV_Comment.from_comment(comment)

        ser = BV_CommentSerializer(bv_comment)

        return Response(ser.data, status=status.HTTP_201_CREATED)
    

    def __str__(self) -> str:
        return self.text

        #("username", "profileImagePreviewUrl", "comment_text", "upvotes")
        #comments = snapshot.comments.all()


class BV_PostView(generics.CreateAPIView):

    serializer_class = BV_PostSerializer

   # permission_classes = (IsAuthenticated,)
    
    def get(self, request,pk=None):

        snapshot = get_object_or_404(Snapshot.objects.all(), pk=1)

        bv_post = BV_Post.from_snapshot(snapshot)

        ser = BV_PostSerializer(bv_post)

        return Response(ser.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk=None):

        profile_me:UserProfile = None
        try:
            profile_me =  UserProfile.get_from_username(request.user.username)
        
        except UserProfile.DoesNotExist:
            return Response({
                "error": "User not found"
            }, status=status.HTTP_401_UNAUTHORIZED)


        ser = BV_PostSerializer(data=request.data)        
        if ser.is_valid() == False:
            return Response({
                "error": "Wrong format"
            }, status=status.HTTP_409_CONFLICT)


       
        title               = ser.data['title']
        description         = ser.data['description']
        author              = profile_me
        location            = None
        upvotes             = 0


        s1 = Snapshot.objects.create(
            title           = title,
            description     = description,
            author          = author,
            location        = location,
            upvotes         = upvotes
        )

        snapshot = None

        try:
            snapshot = Snapshot.objects.get(pk = s1.pk)
        except Snapshot.DoesNotExist:
            return Response({
                "error": "Something went wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if hasattr(ser, 'media'):
            bv_media = ser.data['media']

            bv_media_access_tokens = []
            for bv_media_f in bv_media.value:
                media_access_token = bv_media_f['media_access_token']
                bv_media_access_tokens.append( media_access_token )

            SnapShotMedia.objects.filter(media_access_token__in = bv_media_access_tokens).update(snapshot = snapshot)


        bv_post = BV_Post.from_snapshot(snapshot)
       
        ser = BV_PostSerializer(bv_post)

        return Response(ser.data, status=status.HTTP_201_CREATED)






