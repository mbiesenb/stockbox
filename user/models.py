from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.contrib.auth.models import User
from media.models import ProfileImage




class UserProfile(models.Model):
    user                    = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='profile')
    username                = models.CharField(max_length=150) # TODO: Find other solution
    firstname               = models.CharField(max_length=100)
    lastname                = models.CharField(max_length=100)
    description             = models.CharField(max_length=100)
    current_profile_image   = models.ForeignKey(ProfileImage, on_delete=models.SET_NULL, null=True)
    
    def get_from_username(username):
        profile = UserProfile.objects.get(username=username)
        return profile

    def username_already_exists(username):
        profileExists = True
        userExists = True
        try:
            userProfile = UserProfile.get_from_username(username)
        except UserProfile.DoesNotExist:
            profileExists = False

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            userExists = False
        
        exists = profileExists == True or userExists == True

        return exists
            

    def __str__(self) -> str:
        return self.user

class BV_UserPostPreview(models.Model):
    
    previewUrl = ""
    description = ""
    
    def __init__(self, previewUrl, description):
        self.previewUrl = previewUrl
        self.description = description

    def get_from_snapshots(snapshots):
        posts = []
        for snapshot in snapshots:

            #preview_url = snapshot.media.media_url
            description = snapshot.description

            post = BV_UserPostPreview('preview_url', description)

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

    def from_profile(profile):

        username        = profile.username
        if profile.current_profile_image != None:
            profile_image = profile.current_profile_image.media_access_token
        else:
            profile_image   = "empty"
        userDescription = profile.description
        followers_count = profile.followers.count()
        following_count = profile.following.count()

        snapshots       = profile.snapshots.all()

        posts            = BV_UserPostPreview.get_from_snapshots(snapshots)

        bv_post = BV_User(
            username        =username,
            profile_image   =profile_image,
            userDescription =userDescription,
            followers_count =followers_count,
            following_count =following_count,
            posts = posts
        )

        return bv_post