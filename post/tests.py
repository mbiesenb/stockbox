import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.tests import AuthenticationModelTest
from media.models import BV_MediaUploadResponse, BV_PostMedia
from media.serializers import BV_MediaUploadResponseSerializer, BV_PostMediaSerializer
from post.models import BV_Post
from post.serializers import BV_CommentSerializer, BV_PostSerializer

from user.models import UserProfile
import requests
import json

class PostModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls):


        u1 = User.objects.create_user(username='test_user1', password='password1')
        #u2 = User.objects.create_user(username='test_user2', password='password2')
        #u3 = User.objects.create_user(username='test_user3', password='password3')
        #u4 = User.objects.create_user(username='test_user4', password='password4')
        
        up1 = UserProfile.objects.create(user = u1, username='test_user1', firstname='Test1', lastname='User1')
        #up2 = UserProfile.objects.create(user = u2, username='test_user2', firstname='Test2', lastname='Test2')
        #up3 = UserProfile.objects.create(user = u3, username='test_user3', firstname='Test3', lastname='Test3')
        #up4 = UserProfile.objects.create(user = u4, username='test_user4', firstname='Test4', lastname='Test4')
        
        
    def setUp(self):

        self.credentials = {
            'username': 'test_user1',
            'password': 'password1'
        }

        self.client = APIClient()

        auth_response = self.client.post("/auth/token/", self.credentials, format='json', follow=True)
        token = str(auth_response.data['access'])

        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))


    def test_simple_upload(self):
                
        image1 = AuthenticationModelTest.get_image_file('example1.png')
        image2 = AuthenticationModelTest.get_image_file('example2.png')
        image3 = AuthenticationModelTest.get_image_file('example3.png')
        image4 = AuthenticationModelTest.get_image_file('example4.png')

        image = AuthenticationModelTest.get_image_file('example.png')

        media_upload  = {
            'MEDIA_UPLOAD': image
        }

        media_image_upload = self.client.post("/media/", media_upload, follow=True)


        self.assertEqual(media_image_upload.status_code, 201)

        post = {
            'title': 'Test Snapshot',
            'description': 'This is a test snapshot',
            'media': [
                {
                    'media_access_token': media_image_upload.data[0]["media_access_token"]
                }
            ]
        }
        ### CANNOT TEST MEDIA REFERENCE NOW ########

        post_media_ser =  BV_PostSerializer(post)

        post_upload = self.client.post("/post/", post_media_ser.data, follow=True)

        self.assertEqual(post_upload.status_code, 201)

        post_upload_ser = BV_PostSerializer(data= post_upload.data)

        valid =  post_upload_ser.is_valid()

        self.assertEqual(valid, True)
   
    def test_add_and_show_comments(self):

        post = {
            'title': 'Test Snapshot',
            'description': 'This is a test snapshot'
        }
        commentary1 = {
            'comment_text': 'Random comment'
        }

        post_media_ser =  BV_PostSerializer(post)
        post_upload = self.client.post("/post/", post_media_ser.data, follow=True)
        post_upload_ser = BV_PostSerializer(data= post_upload.data)
        post_upload_ser.is_valid()
        self.assertEqual( post_upload_ser.data['comment_count'] , 0 )
        comment_upload = BV_CommentSerializer(commentary1)
        comment_upload_response = self.client.post("/post/1/comments/", comment_upload.data, follow=True)
        self.assertEqual(comment_upload_response.status_code, 201)
        comment_upload_response = self.client.post("/post/1/comments/", comment_upload.data, follow=True)
        self.assertEqual(comment_upload_response.status_code, 201)
        comment_upload_response = self.client.post("/post/1/comments/", comment_upload.data, follow=True)
        self.assertEqual(comment_upload_response.status_code, 201)

        post_response = self.client.get("/post/1/", "", follow=True)
        self.assertEqual(post_response.status_code, 200)

        post_ser = BV_PostSerializer(data=post_response.data)
        post_ser.is_valid()

        self.assertEqual(post_ser.data['comment_count'], 3)


        comments_response = self.client.get("/post/1/comments/", "", follow=True)
        self.assertEqual(comments_response.status_code, 200)

        comments_response_ser = BV_CommentSerializer(data=comments_response.data, many=True)
        comments_response_ser_valid = comments_response_ser.is_valid( )
        
        self.assertEqual(comments_response_ser_valid, True)
        self.assertEqual( len(comments_response_ser.data) , 3 )










        
        