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



        
        
        
   
