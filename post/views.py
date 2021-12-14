from django.core.exceptions import ValidationError
from django.shortcuts import render
from media.models import BV_MediaUploadResponse, SnapShotMedia
from media.serializers import BV_MediaUploadResponseSerializer
from post.models import BV_Post, Snapshot, BV_Comment
from post.serializers import SnapshotSerializer, BV_PostSerializer, BV_CommentSerializer
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics

from user.models import UserProfile

from django.forms.models import model_to_dict

# Create your views here.

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


class BV_CommentView(generics.CreateAPIView):

    serializer_class = BV_CommentSerializer
    queryset = Snapshot.objects.all()

    def get(self, request, pk=None):

        bv_comments = list()
        snapshot = get_object_or_404( self.queryset , pk=pk)

        comments = snapshot.comments.all()

        bv_comments = list()
        # TODO
        for comment in comments:
            username = comment.author.username
            if comment.author.current_profile_picture != None:
                profileImangePreviewUrl = comment.author.current_profile_picture.media_access_token
            else:
                profileImangePreviewUrl = 'empty'
            comment_text = comment.text
            upvotes = comment.comment_upvotes.count()

            bv_comment = BV_Comment(
                username=username,
                profileImagePreviewUrl=profileImangePreviewUrl,
                comment_text=comment_text,
                upvotes=upvotes
            )

            bv_comments.append(bv_comment)

        ser = BV_CommentSerializer(bv_comments, many=True) 
        #ser.is_valid(raise_exception=True)
        return Response(ser.data)

class BV_PostUpload(generics.CreateAPIView):
    serializers
class BV_PostView(generics.CreateAPIView):

    serializer_class = BV_PostSerializer
    
    def get(self, request,pk=None):

        snapshot = get_object_or_404(Snapshot.objects.all(), pk=1)

        bv_post = BV_Post.from_snapshot(snapshot)

        ser = BV_PostSerializer(bv_post)

        return Response(ser.data)
    
    def post(self, request, pk=None):

        #Needed Fields
        #media_access_token
        ser = BV_PostSerializer(request.data)
        
        #newPost = ser.data
        username = 'user1'
        profile_me = UserProfile.get_from_username(username)

        #media_access_tokens = BV_MediaUploadResponseSerializer(
        #    data= newPost['media_access_tokens'],
        #    many=True
        #)

        title               = ser['title']
        description         = ser['description']
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

        bv_media = ser['media']

        bv_media_access_tokens = []
        for bv_media_f in bv_media.value:
            media_access_token = bv_media_f['media_access_token']
            bv_media_access_tokens.append( media_access_token )


        snapshot = Snapshot.objects.get(pk = s1.pk)

        SnapShotMedia.objects.filter(media_access_token__in = bv_media_access_tokens).update(snapshot = snapshot)

        #RELOAD SNAPSHOT --> Not efficient --> fix in the future


        bv_post = BV_Post.from_snapshot(snapshot)
       
        ser = BV_PostSerializer(bv_post)

        return Response(ser.data)

        


        

        #title = models.CharField(max_length=100)
        #description = models.CharField(max_length=100)
        #author = models.ForeignKey(
        #    UserProfile, on_delete=models.SET_NULL, related_name='snapshots', null=True)
        #location = models.ForeignKey(
        #    Location, on_delete=models.SET_NULL, null=True)
        #upvotes = models.IntegerField()

        #def __str__(self) -> str:
        #    return self.title





