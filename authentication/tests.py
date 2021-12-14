from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from user.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

from io import BytesIO
from PIL import Image
from django.core.files.base import File

# Create your tests here.
class MessageModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls):
        u1 = User.objects.create_user(username='test_user1', password='password1')
        u2 = User.objects.create_user(username='test_user2', password='password2')
        u3 = User.objects.create_user(username='test_user3', password='password3')
        u4 = User.objects.create_user(username='test_user4', password='password4')
        
        up1 = UserProfile.objects.create(user = u1, username='test_user1', firstname='Test1', lastname='User1', current_profile_image = None)
        up2 = UserProfile.objects.create(user = u2, username='test_user2', firstname='Test2', lastname='Test2', current_profile_image = None)
        up3 = UserProfile.objects.create(user = u3, username='test_user3', firstname='Test3', lastname='Test3', current_profile_image = None)
        up4 = UserProfile.objects.create(user = u4, username='test_user4', firstname='Test4', lastname='Test4', current_profile_image = None)

    @staticmethod
    def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.client = APIClient()

    
    def test_receive_acces_token(self):
        
        
        auth_response = self.client.post("/auth/token/", {
            'username': 'test_user1',
            'password': 'password1'
        }, format='json', follow=True)

        self.assertEqual(auth_response.status_code , 200)

        auth_response = self.client.post("/auth/token/", {
            'username': 'test_user1xxxxxxx',
            'password': 'password1'
        }, format='json', follow=True)
        self.assertEqual(auth_response.status_code , 401) #NOT AUTORIZED

        auth_response = self.client.post("/auth/token/", {
            'password': 'password1'
        }, format='json', follow=True)
        self.assertEqual(auth_response.status_code , 400) #BAD REQUEST

    def test_refresh_access_token(self):
        
        auth_response = self.client.post("/auth/token/", {
            'username': 'test_user1',
            'password': 'password1'
        }, format='json', follow=True)

        token_access = str(auth_response.data['access'])
        token_refresh = str(auth_response.data['refresh'])

        auth_response = self.client.post("/auth/token/refresh/", {
            'refresh': token_refresh
        }, format='json', follow=True)
        self.assertEqual(auth_response.status_code , 200)

        auth_response = self.client.post("/auth/token/refresh/", {
            'refresh': token_refresh
        }, format='json', follow=True)
        self.assertEqual(auth_response.status_code , 200)

        auth_response = self.client.post("/auth/token/refresh/", {
            'refresh': 'xxx'
        }, format='json', follow=True)
        self.assertEqual(auth_response.status_code , 401)

        auth_response = self.client.post("/auth/token/refresh/", {
            'refresh_xxx': token_refresh
        }, format='json', follow=True)
        self.assertEqual(auth_response.status_code , 400)

    def test_verify(self):

        auth_response = self.client.post("/auth/token/", {
            'username': 'test_user1',
            'password': 'password1'
        }, format='json', follow=True)

        token_access = str(auth_response.data['access'])
        token_refresh = str(auth_response.data['refresh'])

        verify_response = self.client.post("/auth/token/verify/", {
            'token': token_access
        }, format='json', follow=True)

        self.assertEqual(verify_response.status_code , 200)
    
    def test_register(self):

        image = self.get_image_file('example.png')

        img_upload  = {
            'MEDIA_UPLOAD': image
        }

        profile_image_upload = self.client.post("/mediapost/profileimage/", img_upload, follow=True)
        
        self.assertEqual(profile_image_upload.status_code, 201 )

        media_access_token = profile_image_upload.data['media_access_token']

        register_request = self.client.post("/auth/register/",{
            "username": "test_username",
            "password": "test_password",
            "password2": "test_password",
            "firstname": "Test",
            "lastname": "User",
            "description": "This is a Test User",
            "profile_image": media_access_token
        }, format='json', follow=True)

        self.assertEqual(register_request.status_code , 201)
        self.assertEqual(register_request.data['profile_image'], media_access_token)

        url = "/mediapost/profileimage/?MEDIA_ACCESS_TOKEN="+str(media_access_token)
        profile_image_request = self.client.get(url)

        self.assertEqual(profile_image_request.status_code, 200)
        

        

        
        





