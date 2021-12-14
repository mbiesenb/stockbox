import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime
from core.models import BV_Chat, Chat, Message
from django.utils import timezone
from core.serializers import BV_ChatSerializer
from user.models import UserProfile
from rest_framework.test import APIClient

# Create your tests here.

class MessageModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls):


        u1 = User.objects.create_user(username='test_user1', password='password1')
        u2 = User.objects.create_user(username='test_user2', password='password2')
        u3 = User.objects.create_user(username='test_user3', password='password3')
        u4 = User.objects.create_user(username='test_user4', password='password4')
        
        up1 = UserProfile.objects.create(user = u1, username='test_user1', firstname='Test1', lastname='User1')
        up2 = UserProfile.objects.create(user = u2, username='test_user2', firstname='Test2', lastname='Test2')
        up3 = UserProfile.objects.create(user = u3, username='test_user3', firstname='Test3', lastname='Test3')
        up4 = UserProfile.objects.create(user = u4, username='test_user4', firstname='Test4', lastname='Test4')
        
        
    def setUp(self):

        self.credentials = {
            'username': 'test_user1',
            'password': 'password1'
        }

        self.client = APIClient()

        auth_response = self.client.post("/auth/token/", self.credentials, format='json', follow=True)
        token = str(auth_response.data['access'])

        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))


    def test_write_message(self):
        
        write_message = {
            "message_text": "newHello, I bims",
            "receiver_username" : "test_user2"
        }

        new_message_response = self.client.post("/core/chats/", write_message, format='json', follow=True)
    
        self.assertEqual(new_message_response.status_code, 201)

        bv_new_message = new_message_response.data

        self.assertEqual( bv_new_message["sender_username"] , "test_user1")
        self.assertEqual( bv_new_message["receiver_username"] , "test_user2")

    def test_chat_create(self):
        
        self.client.post("/core/chats/", {
            "message_text": "newHello, I bims",
            "receiver_username" : "test_user2"
        }, format='json', follow=True)

        bv_chats = self.client.get("/core/chats/", follow=True).data
        self.assertEqual(len(bv_chats) , 1)

        self.client.post("/core/chats/", {
            "message_text": "newHello, I bims",
            "receiver_username" : "test_user2"
        }, format='json', follow=True)
        
        bv_chats = self.client.get("/core/chats/", follow=True).data
        self.assertEqual(len(bv_chats) , 1)

        self.client.post("/core/chats/", {
            "message_text": "newHello, I bims",
            "receiver_username" : "test_user3"
        }, format='json', follow=True)
        
        bv_chats = self.client.get("/core/chats/", follow=True).data
        self.assertEqual(len(bv_chats) , 2)

        self.client.post("/core/chats/", {
            "message_text": "newHello, I bims",
            "receiver_username" : "test_user4"
        }, format='json', follow=True)
        
        bv_chats = self.client.get("/core/chats/", follow=True).data
        self.assertEqual(len(bv_chats) , 3)


    def test_show_last_message(self):

        write_message = {
            "message_text": "This should be the last message",
            "receiver_username" : "test_user2"
        }

        self.client.post("/core/chats/", write_message, format='json', follow=True)

        chat_response = self.client.get("/core/chats/", follow=True)

        self.assertEqual(chat_response.status_code, 200)


        bv_chats = chat_response.data

        self.assertEqual(len(bv_chats) , 1)


        self.assertEqual( bv_chats[0]["latest_message_text"] ,  "This should be the last message" )
        self.assertEqual( bv_chats[0]["latest_message_username"] ,  "test_user1" )


    def test_show_chat_history(self):
        self.client.post("/core/chats/", { 
            "message_text": "Spam 1",
            "receiver_username" : "test_user2"
        }, format='json', follow=True)
    
        self.client.post("/core/chats/", { 
            "message_text": "Spam 2",
            "receiver_username" : "test_user2"
        }, format='json', follow=True)

        self.client.post("/core/chats/", { 
            "message_text": "Spam 3",
            "receiver_username" : "test_user2"
        }, format='json', follow=True)

        self.client.post("/core/chats/", { 
            "message_text": "Spam 4",
            "receiver_username" : "test_user2"
        }, format='json', follow=True)

        chat_response = self.client.get("/core/chats/1/messages", follow=True)

        bv_messages = chat_response.data

        self.assertEqual(len(bv_messages) , 4)   
