from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
import os
from PIL import Image
from media.models import BV_MediaUploadResponse, MediaImage, ProfileImage, SnapShotMedia
from media.serializers import BV_MediaUploadResponseSerializer
from stockbox.settings import BASE_DIR
from django.shortcuts import get_object_or_404
import sys
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class BV_MediaView(APIView):
    
    __TESTING__ = sys.argv[1:2] == ['test']

    permission_classes = (IsAuthenticated,)
    
    def get(self, request,pk=None):
        media_access_token = request.GET.get('MEDIA_ACCESS_TOKEN', '')

        if media_access_token == '':
            return HttpResponseNotFound("MEDIA_ACCESS_TOKEN not set")
        
        snapshotMedia = get_object_or_404( SnapShotMedia, media_access_token = media_access_token )

        media_path = SnapShotMedia.get_path_from_media_access_token(snapshotMedia.content_type, snapshotMedia.media_access_token)

        response = HttpResponse(
            content_type= SnapShotMedia.get_contenttype_by_filetype(
                filetype= SnapShotMedia.get_filetype_by_contenttype( snapshotMedia.content_type)
            )  
        )

        if self.__TESTING__ == False:
            pil_img = Image.open( media_path )
            pil_img.save(response, SnapShotMedia.get_filetype_by_contenttype( snapshotMedia.content_type ))

        return response


    def post(self, request, pk=None):
        

        bv_uploads = list()
        for f in request.FILES.getlist('MEDIA_UPLOAD'):

            name = f.name
            content_type = f.content_type
            size = f.size

            if content_type.startswith("image/"):
                
                storage_path_img = 'media/storage/images'
                media_access_token = str( uuid.uuid4().hex )
                storage_filetype = 'PNG'

                media_path = SnapShotMedia.get_path_from_media_access_token(
                    content_type = content_type,
                    media_access_token= media_access_token
                )

                pil_img = Image.open( f.file )                
                if self.__TESTING__ == False:
                    pil_img.save(media_path)

                #TODO: Choose an other identifier for image
                bv_mediaUpload_Response = BV_MediaUploadResponse(
                    media_upload_key = name,
                    media_access_token = media_access_token,
                    upload_success = True,
                    upload_message=""
                )
                
                media_image = MediaImage.objects.create(
                    img_x = pil_img.size[0],
                    img_y = pil_img.size[1]
                )

                snapshot_media = SnapShotMedia.objects.create(
                    snapshot = None,
                    content_type = content_type,
                    media_access_token = media_access_token,
                    media_image = media_image,
                    media_video = None
                )

                bv_uploads.append(bv_mediaUpload_Response)


        ser = BV_MediaUploadResponseSerializer(bv_uploads , many=True)

        return Response(ser.data, status=status.HTTP_201_CREATED)


class BV_ProfileImageView(APIView):

    __TESTING__ = sys.argv[1:2] == ['test']
        
    permission_classes = (IsAuthenticated,)

    def get(self, request,pk=None):
        media_access_token = request.GET.get('MEDIA_ACCESS_TOKEN', '')

        if media_access_token == '':
            return HttpResponseNotFound("MEDIA_ACCESS_TOKEN not set")
            
        snapshotMedia = get_object_or_404( ProfileImage, media_access_token = media_access_token )

        media_path = ProfileImage.get_path_from_media_access_token(snapshotMedia.media_access_token)

        response = HttpResponse(
            content_type= 'image/png'
        )

        if self.__TESTING__ == False:
            pil_img = Image.open( media_path )
            pil_img.save(response,  'PNG')

        return response


    def post(self, request, pk=None):
            
            
        uploads = request.FILES.getlist('MEDIA_UPLOAD')
        if len(uploads) == 0:
            # TODO: Return error code here
            pass

        uploaded_file = uploads[0]
        if uploaded_file.content_type.startswith("image/"):
            media_access_token = str( uuid.uuid4().hex )

            media_path = ProfileImage.get_path_from_media_access_token(
                media_access_token= media_access_token
            )

            if self.__TESTING__ == False:
                pil_img = Image.open( uploaded_file.file )
                pil_img.save(media_path)
                


            bv_mediaUpload_Response = BV_MediaUploadResponse(
                    media_upload_key = uploaded_file.name,
                    media_access_token = media_access_token,
                    upload_success = True,
                    upload_message=""
            )

            ProfileImage.objects.create(
                media_access_token = media_access_token,
                profile = None
            )

                
            ser = BV_MediaUploadResponseSerializer(bv_mediaUpload_Response)

            return Response(ser.data, status=status.HTTP_201_CREATED)

        else:
            # TODO: Return error code here
            pass

        
                




