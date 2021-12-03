from django.db import models

import user


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