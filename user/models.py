from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import IntegerField
from django.contrib.auth.models import User
import user

class UserImage(models.Model):
    filename = models.CharField(max_length=50)
    filetype = models.CharField(max_length=10)
    img_x = models.IntegerField()
    img_y = models.IntegerField() 
    #pic = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self) -> str:
        return self.filename + "." + self.filetype


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='profile')
    username = models.CharField(max_length=150) # TODO: Find other solution
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    pic = models.ForeignKey(UserImage, on_delete=models.SET_NULL, null=True)
    
    def get(username):
        #try:
        #    profile = UserProfile.objects.get(username=username)
        #except ObjectDoesNotExist:
        #    return None
        #
        #return profile
        profile = UserProfile.objects.get(username=username)
        return profile

    def __str__(self) -> str:
        return self.user

#//Business View: UserProfile
#+ Username
#+ UserProfile
#+ UserDescription
#+ Followers - Cout
#+ Following - Cout
#+ Posts
#    + PostImage/Video - Preview
# toggle_followship
# show_messages

class BV_UserPostPreview(models.Model):
    
    previewUrl = ""
    description = ""
    
    def __init__(self, previewUrl, description):
        self.previewUrl = previewUrl
        self.description = description

    def get_from_snapshots(snapshots):
        posts = []
        for snapshot in snapshots:

            preview_url = snapshot.media.media_url
            description = snapshot.description

            post = BV_UserPostPreview(preview_url, description)

            posts.append(post)

        return posts


    class Meta:
        managed = False

# Create your models here.
class BV_User(models.Model):
    username = ""
    profile_image = ""
    userDescription = ""
    followers_count = 0
    following_count  = 0
    posts = list()

    def __init__(self, username, profile_image, userDescription, followers_count, following_count, posts=None):
        self.username = username
        self.profile_image = profile_image
        self.userDescription = userDescription
        self.followers_count = followers_count
        self.following_count = following_count
        self.posts = posts

    class Meta:
        managed = False