from django.shortcuts import render
from post.models import BV_Post, Snapshot, BV_Comment
from post.serializers import SnapshotSerializer, BV_PostSerializer, BV_CommentSerializer
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics

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
            profileImangePreviewUrl = comment.author.pic.filename
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


class BV_PostView(generics.CreateAPIView):

    serializer_class = BV_PostSerializer
    
    def get(self, request,pk=None):
        snapshot = get_object_or_404(Snapshot.objects.all(), pk=1)
        media_url       = snapshot.media.media_url
        media_type      = snapshot.media.media_type
        upvotes         = snapshot.snapshot_upvotes.count()
        comment_count   = snapshot.comments.count()
        profile         = snapshot.author
        tags            = snapshot.tags
        bv_post = BV_Post(
            psnapshot=snapshot,
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
