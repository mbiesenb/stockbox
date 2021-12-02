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


# Create your models here.
class BV_User(models.Model):
    username = ""
    userDescription = ""
    followers_count = 0
    following_count  = 0
    posts = list()

    def __init__(self, username, userDescription, followers_count, following_count, posts=None):
        self.username = username
        self.userDescription = userDescription
        self.followers_count = followers_count
        self.following_count = following_count
        self.posts = posts

    class Meta:
        managed = False