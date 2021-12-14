from colorama.ansi import Fore
from colorama import init, Fore, Back, Style
import requests
from django.core.management.base import BaseCommand, CommandError
import json

class Command(BaseCommand):

    def add_argument(self, parser):
        pass
        #parser.add_argument('')
    def handle(self, *args, **options):
        
        init(autoreset=True)

        user_credentials = {
            "username": "user1",
            "password": "password1"
        }
        token = requests.post("http://localhost:8000/auth/token/", data=user_credentials)
        token_d = json.loads(token.text)
        print(Fore.GREEN+"Access-Token: ")
        print(token_d["access"])
        print(Fore.GREEN+"Refresh-Token: ")
        print(token_d["refresh"])

        ## Display Chats
        url = "http://localhost:8000/core/chats/"
        response = requests.request("GET", url)
        print(Fore.GREEN+"Current Chats:")
        print(response.text)

        ## Create a new Message
        url = "http://localhost:8000/core/chats/"
        payload = json.dumps({
        "message_text": "newHello, I bims",
        "receiver_username": "user3"
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(Fore.GREEN+"New Message Item:")
        print(response.text)

        ## Get first Chat History
        url = "http://localhost:8000/core/chats/1/messages"

        response = requests.request("GET", url)
        print(Fore.GREEN+"Chat History:")
        print(response.text)

        ## POST SOME FANCY MEDIA
        url = "http://localhost:8000/media/"

        payload={}
        files=[
        ('MEDIA_UPLOAD',('black_white.jpg',open('C:/Users/Marvin/Desktop/Hintergrundbilder/Leon/black_white.jpg','rb'),'image/jpeg')),
        ('MEDIA_UPLOAD',('wallpaperbetter.jpg',open('C:/Users/Marvin/Desktop/Hintergrundbilder/Leon/wallpaperbetter.jpg','rb'),'image/jpeg')),
        ('MEDIA_UPLOAD',('red.jpg',open('C:/Users/Marvin/Desktop/Hintergrundbilder/Leon/red.jpg','rb'),'image/jpeg')),
        ('MEDIA_UPLOAD',('central.png',open('C:/Users/Marvin/Desktop/Hintergrundbilder/Leon/central.png','rb'),'image/png'))
        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        media_access_tokens = json.loads(response.text)

        print(Fore.GREEN+"Media Upload Response Tokens")
        for media_access_token in media_access_tokens:
            media_access_token_d = media_access_token['media_access_token']
            print(media_access_token_d)

        media_access_token= json.loads(response.text)[0]['media_access_token']



        ## GET ONE IMAGE
        url = "http://localhost:8000/media/?MEDIA_ACCESS_TOKEN="+str(media_access_token)

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        print(Fore.GREEN+"Media download status code")
        print(response.status_code )


        ## Upload Post and connect to media
        url = "http://localhost:8000/post/"

        payload = json.dumps({
            "title": "Snapshot1",
            "description": "This is Snapshot 1",
            "media": media_access_tokens
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        
        
        
   
