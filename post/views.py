from django.shortcuts import render
from post.models import Snapshot
from post.serializers import SnapshotSerializer
from rest_framework.response import Response
from rest_framework import viewsets
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


class BV_PostView(generics.CreateAPIView):

    serializer_class = BV_PostSerializer
    #queryset = Snapshot.objects.all()
    
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

