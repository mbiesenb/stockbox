from rest_framework.response import Response
from rest_framework import generics
from core import serializers
from core.models import BV_Chat, BV_ChatMessage, Chat, Message
from user.models import UserProfile
from core.serializers import BV_ChatMessageSerializer, BV_ChatSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.
# http://www.tomchristie.com/rest-framework-2-docs/api-guide/routers

class BV_ChatView(generics.CreateAPIView):

    serializer_class = BV_ChatSerializer
    queryset  = Chat.objects.all()

    def get(self, request,pk=None):

        username = request.user.username
        #REMOVE THIS STATIC USER HERE
        username = 'user1'

        profile_me = UserProfile.get(username)

        chats1 = profile_me.chats1.all()
        chats2 = profile_me.chats2.all()
        chats = chats1.union(chats2)

        bv_chats  = list()
        for chat in chats.all():
            latest_message = chat.messages.latest('timestamp')

            latest_message_text = latest_message.text
            latest_message_timestamp = latest_message.timestamp
            latest_message_username = latest_message.sender.username
            
            user1 = chat.user1
            user2 = chat.user2

            partner_user = None
            if user1 == profile_me.username:
                partner_user = user2
            else:
                partner_user = user1
            
            partner_username = partner_user.username
            partner_profileImage = partner_user.pic.filename

            unread_messages_count = chat.messages.filter(read_status = 0, receiver=profile_me).count()

            bv_chat = BV_Chat(
                partner_username = partner_username,
                partner_profileImage = partner_profileImage,
                latest_message_username=latest_message_username,
                latest_message_text = latest_message_text,
                latest_message_timestamp = latest_message_timestamp,
                unread_message_count= unread_messages_count
            )

            bv_chats.append(bv_chat)

        #bv_chats.sort(key=latest_message_timestamp)

        ser = BV_ChatSerializer(bv_chats, many=True)
        #ser.is_valid(raise_exception=True)
        return Response(ser.data)


class BV_ChatMessageView(generics.CreateAPIView):

    serializer_class = BV_ChatMessageSerializer
    queryset  = Chat.objects.all()


    def get(self, request,chat_id=None):

        username_me = request.user.username

        chat = get_object_or_404(Chat.objects.all(), pk=chat_id)

        messages = chat.messages

        bv_chatmessages = list()

        for message in messages.all():
            username = message.sender.username
            sender_image = message.sender.pic.filename
            if username == username_me:
                me = "X"
            else:
                me = ""
            message_text = message.text
            message_time = message.timestamp

            bv_chatmessage = BV_ChatMessage(
                username = username,
                sender_image = sender_image,
                me = me,
                message_text =  message_text,
                message_time = message_time
            )

            bv_chatmessages.append(bv_chatmessage)

        ser = BV_ChatMessageSerializer(bv_chatmessages, many=True)
        #ser.is_valid(raise_exception=True)
        return Response(ser.data)
