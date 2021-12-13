from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from user.models import UserProfile

# Create your tests here.
class MessageModelTest(TestCase):
    

    @classmethod
    def setUpTestData(cls):
        u1 = User.objects.create_user(username='test_user1', password='password1')
        u2 = User.objects.create_user(username='test_user2', password='password2')
        u3 = User.objects.create_user(username='test_user3', password='password3')
        u4 = User.objects.create_user(username='test_user4', password='password4')
        
        up1 = UserProfile.objects.create(user = u1, username='test_user1', firstname='Test1', lastname='User1', pic = None)
        up2 = UserProfile.objects.create(user = u2, username='test_user2', firstname='Test2', lastname='Test2', pic = None)
        up3 = UserProfile.objects.create(user = u3, username='test_user3', firstname='Test3', lastname='Test3', pic = None)
        up4 = UserProfile.objects.create(user = u4, username='test_user4', firstname='Test4', lastname='Test4', pic = None)

    
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


