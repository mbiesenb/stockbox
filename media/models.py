from django.db import models
#from post.models import Snapshot
#from user.models import UserProfile

# Create your models here.
class BV_MediaUploadResponse(models.Model):

    #this value is a identifier for the user
    #with this value, the uploader can map the upload response with the uploaded files
    media_upload_key    = ""
    media_access_token  = ""
    upload_success      = False
    upload_message      = ""

    class Meta:
        managed = False

    def __init__(self, media_upload_key, media_access_token, upload_success, upload_message):
        self.media_upload_key   = media_upload_key
        self.media_access_token = media_access_token
        self.upload_success     = upload_success
        self.upload_message     = upload_message


class MediaImage(models.Model):
    img_x = models.IntegerField()
    img_y = models.IntegerField()

    def __str__(self) -> str:
        return "image"


class MediaVideo(models.Model):
    duration = models.IntegerField()

    def __str__(self) -> str:
        return "video"


class ProfileImage(models.Model):
    media_access_token  = models.CharField(max_length=50, default='', unique=True)
    profile = models.ForeignKey( to='user.UserProfile', on_delete=models.SET_NULL, related_name='profile_image', null=True )

    def __str__(self) -> str:
        return self.media_access_token

    def get_path_from_media_access_token(media_access_token):
        storage_path_img = 'media/storage/profileimages'
        return str(storage_path_img + '/' + media_access_token + '.' + 'PNG' )


class SnapShotMedia(models.Model):
    snapshot            = models.ForeignKey(to='post.Snapshot', on_delete=models.SET_NULL, related_name='media', null=True)
    content_type        = models.CharField(max_length=50, default='')
    media_access_token  = models.CharField(max_length=50, default='', unique=True)
    media_image         = models.ForeignKey(MediaImage, on_delete=models.SET_NULL, related_name='media_image', null=True)
    media_video         = models.ForeignKey( MediaVideo, on_delete=models.SET_NULL, related_name='media_video', null=True)

    def __str__(self) -> str:
        
        return self.type
    
    def  get_contenttype_by_filetype(filetype):

        if filetype == 'PNG':
            return 'image/png'
        else:
            return ''

    def get_filetype_by_contenttype(content_type):

        if content_type.startswith("image/"):
            return 'PNG'
        else:
            pass

    def get_path_from_media_access_token(content_type, media_access_token):
         if content_type.startswith("image/"):

            storage_path_img = 'media/storage/images'
            return str(storage_path_img + '/' + media_access_token + '.' + SnapShotMedia.get_filetype_by_contenttype(content_type) )

         else:
             return str('')

class BV_PostMedia(models.Model):

    media_access_token = ""
    #content_type = ""

    class Meta:
        managed = False