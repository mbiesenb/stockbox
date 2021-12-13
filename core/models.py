from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields import IntegerField
from django.db.models.query_utils import Q
from post.models import Snapshot, Comment
from user.models import UserProfile
# Create your models here.


class Tag(models.Model):
    text        = models.CharField(max_length=30)
    snapshot    = models.ForeignKey(Snapshot, related_name='tags', on_delete=models.SET_NULL, null=True) 
    author      = models.ForeignKey(UserProfile , on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.text




# When a user writes a message, the api generates two entries in chat model
# one with user1 = u1 , user2 = u2 and one for user1 = u2, user2 = u1
class Chat(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=SET_NULL, related_name='chats1', null=True)
    user2 = models.ForeignKey(UserProfile, on_delete=SET_NULL, related_name='chats2', null= True)


    def get_by_participants(u1, u2):
        chat = Chat.objects.filter( Q(user1 = u1 , user2=u2)  | Q(user1 = u2 , user2 = u1) )

        if len( chat ) == 1:
            return chat[0]
        else:
            return None

class Message(models.Model):
    chat        = models.ForeignKey(Chat, on_delete=SET_NULL, related_name='messages', null=True)
    sender      = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='message_sent' ,null=True)
    receiver    = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='message_received',null=True)
    text        = models.CharField(max_length=500)
    read_status = models.IntegerField( default=0)
    timestamp   = models.DateTimeField(null=True)

class Follow(models.Model):
    follower    = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='following',null=True)
    stalker     = models.ForeignKey(UserProfile, on_delete=SET_NULL,related_name='followers',null=True)

class Upvote(models.Model):
    upvoter     = models.ForeignKey(UserProfile, on_delete=SET_NULL, related_name='upvoter', null=True)
    type        = models.IntegerField() #1 = tag, 2=comment, 3 = snapshot
    tag         = models.ForeignKey(Tag, on_delete=SET_NULL, related_name='tag_upvotes', null=True)
    comment     = models.ForeignKey(Comment, on_delete=SET_NULL, related_name='comment_upvotes', null=True)
    snapshot    = models.ForeignKey(Snapshot, on_delete=SET_NULL, related_name='snapshot_upvotes', null=True)


class BV_Chat(models.Model):
    partner_username = ""
    partner_profileImage = ""
    latest_message_username = ""
    latest_message_text = ""
    latest_message_timestamp = ""
    unread_message_count = 0


    def __init__(self, partner_username, partner_profileImage, latest_message_username, latest_message_text, latest_message_timestamp, unread_message_count):
        self.partner_username = partner_username
        self.partner_profileImage = partner_profileImage
        self.latest_message_username = latest_message_username
        self.latest_message_text = latest_message_text
        self.latest_message_timestamp = latest_message_timestamp
        self.unread_message_count = unread_message_count

    class Meta:
        managed = False



class BV_ChatMessage(models.Model):
    sender_username     = ""
    receiver_username   = ""
    sender_image        = ""
    #me = ""
    message_text        = ""
    message_time        = ""

    def __init__(self, sender_username, receiver_username, sender_image, message_text, message_time):
        self.sender_username    = sender_username
        self.receiver_username  = receiver_username
        self.sender_image       = sender_image
        #self.me = me
        self.message_text       = message_text
        self.message_time       = message_time
    
    def from_db_message(message):
        sender_username     = message.sender.username
        receiver_username   = message.receiver.username
        if message.sender.pic != None:
            sender_image    = message.sender.pic.filename
        else:
            sender_image    = 'empty'

        message_text = message.text
        message_time = message.timestamp

        bv_chatmessage = BV_ChatMessage(
            sender_username     = sender_username,
            receiver_username   = receiver_username,
            sender_image        = sender_image,
            message_text        =  message_text,
            message_time        = message_time
        )

        return bv_chatmessage

    class Meta:
        managed = False

class BV_ChatMessageSend(models.Model):
    message_text = ""
    receiver_username = ""

    def __init__(self, message_text):
        self.message_text = message_text
    
    class Meta:
        managed = False

