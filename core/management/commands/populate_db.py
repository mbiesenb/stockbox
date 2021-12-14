from core.models import  Chat, Upvote, UserProfile, Comment, Follow,Snapshot, Message, Tag
from post.models import  Location
from media.models import ProfileImage
from media.models import MediaImage, MediaVideo, SnapShotMedia
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.core.management import call_command
from django.contrib.auth.models import User
from colorama import init, Fore, Back, Style
from pathlib import Path
from datetime import datetime
from django.utils import timezone
import shutil
import os

class Command(BaseCommand):

    help = 'Inserts dummy records'

    def add_arguments(self, parser):

        #pass
        parser.add_argument('-a', '--andy', type=str, help='Option after executing (run = Run Server | apply = Run Server and Apply Requests)' )

    def handle(self, *args, **options):
        
        and_option = options['andy']

        init(autoreset=True)
        
        #1-2. DROP DATABASE
        print(Fore.GREEN+"1-2.DROP DATABASE")
        if os.path.exists("db.sqlite3"):
            os.system('del db.sqlite3')
            #exec("rm db.sqlite3")

        #3. Remove all migrations and files
        print(Fore.GREEN+"3.DELETE MIGRATIONS ON FS")
        if Path('core/migrations').exists():
            shutil.rmtree('core/migrations')
        os.mkdir('core/migrations')
        open('core/migrations/__init__.py','w').close()

        if Path('authentication/migrations').exists():
            shutil.rmtree('authentication/migrations')
        os.mkdir('authentication/migrations')
        open('authentication/migrations/__init__.py','w').close()

        if Path('post/migrations').exists():
            shutil.rmtree('post/migrations')
        os.mkdir('post/migrations')
        open('post/migrations/__init__.py','w').close()

        if Path('user/migrations').exists():
            shutil.rmtree('user/migrations')
        os.mkdir('user/migrations')
        open('user/migrations/__init__.py','w').close()

        if Path('media/migrations').exists():
            shutil.rmtree('media/migrations')
        os.mkdir('media/migrations')
        open('media/migrations/__init__.py','w').close()

        if Path('media/storage/images').exists():
            shutil.rmtree('media/storage/images')
        os.mkdir('media/storage/images')
       


        #4. Create Initial Migration
        print(Fore.GREEN+"4.RUN MIGRATIONS")
        call_command('makemigrations')
        call_command('migrate')

        #5 Population Database with new Data
#Location, UserProfile, Comment, Follow,Snapshot, Message, Tag, ProfileImage

        print(Fore.GREEN+"4.POPULATE DB")
        print(Fore.GREEN+"4.1.INSERT USER")
        admin = User.objects.create_user(username='admin', password='admin', is_superuser=True)
        u1 = User.objects.create_user(username='user1', password='password1')
        u2 = User.objects.create_user(username='user2', password='password2')
        u3 = User.objects.create_user(username='user3', password='password3')

        print(Fore.GREEN+"4.2.INSERT USERPROFILE")
        up1 = UserProfile.objects.create(user = u1, username='user1', firstname='Firstname1', lastname='lastname1')
        up2 = UserProfile.objects.create(user = u2, username='user2', firstname='Firstname2', lastname='lastname2')
        up3 = UserProfile.objects.create(user = u3, username='user3', firstname='Firstname3', lastname='lastname3')
      
        print(Fore.GREEN+"4.3.INSERT PROFILEIMAGE")
        ui1 = ProfileImage.objects.create( media_access_token = 'file1', profile=up1 )
        ui2 = ProfileImage.objects.create( media_access_token = 'file2', profile=up2 )
        ui3 = ProfileImage.objects.create( media_access_token = 'file3', profile=up3 )

        print(Fore.GREEN+"4.4.INSERT LOCATION")
        l1 = Location.objects.create( longitude="444", latitude="999",locationText="Berlin" )
        l2 = Location.objects.create( longitude="444", latitude="999",locationText="Zürich" )
        l3 = Location.objects.create( longitude="444", latitude="999",locationText="Wien" )

        print(Fore.GREEN+"4.5.1 INSERT MEDIAIMAGE")
        mi1 = MediaImage.objects.create( img_x = 100, img_y = 100)
        mi2 = MediaImage.objects.create( img_x = 200, img_y = 400)


        print(Fore.GREEN+"4.5.2 INSERT MEDIAVIDEO")
        mv1 = MediaVideo.objects.create( duration = 120 )
        mv2 = MediaVideo.objects.create( duration = 180 )


        print(Fore.GREEN+"4.6.INSERT SNAPSHOT")
        s1 = Snapshot.objects.create( title = 'Snapshot1' , description = 'This is Snapshot 1', author = up1, location = l1, upvotes =101)
        s2 = Snapshot.objects.create( title = 'Snapshot2' , description = 'This is Snapshot 2', author = up1, location = l2, upvotes =102)
        s3 = Snapshot.objects.create( title = 'Snapshot3' , description = 'This is Snapshot 3', author = up1, location = l3, upvotes =103)


        print(Fore.GREEN+"4.5.3 INSERT SNAPSHOTMEDIA")
        sm1 = SnapShotMedia.objects.create( content_type = 1, media_access_token='ababababababab',  media_image=mi1, media_video=None, snapshot=s1)
        sm2 = SnapShotMedia.objects.create( content_type = 1, media_access_token='acacacacacacac',  media_image=mi2, media_video=None, snapshot=s1)
        sm3 = SnapShotMedia.objects.create( content_type = 2, media_access_token='adadadadadadad',  media_image=None, media_video=mv1, snapshot=s1)

        print(Fore.GREEN+"4.7.INSERT COMMENT")
        c11 = Comment.objects.create( text = 'Random Comment 1', snapshot=s1,  author=up1, upvotes=1)
        c12 = Comment.objects.create( text = 'Random Comment 2', snapshot=s1,  author=up2, upvotes=2)
        c13 = Comment.objects.create( text = 'Random Comment 3', snapshot=s1,  author=up3, upvotes=3)
        c21 = Comment.objects.create( text = 'Random Comment 1', snapshot=s2,  author=up1, upvotes=1)
        c22 = Comment.objects.create( text = 'Random Comment 2', snapshot=s2,  author=up2, upvotes=2)
        c23 = Comment.objects.create( text = 'Random Comment 3', snapshot=s2,  author=up3, upvotes=3)
        c31 = Comment.objects.create( text = 'Random Comment 1', snapshot=s3,  author=up1, upvotes=1)
        c32 = Comment.objects.create( text = 'Random Comment 2', snapshot=s3,  author=up2, upvotes=2)
        c33 = Comment.objects.create( text = 'Random Comment 3', snapshot=s3,  author=up3, upvotes=3)

        print(Fore.GREEN+"4.8.INSERT TAG")
        t11 = Tag.objects.create( text = 'Random Tag 1', author=up1, snapshot=s1)
        t12 = Tag.objects.create( text = 'Random Tag 2', author=up2, snapshot=s1)
        t13 = Tag.objects.create( text = 'Random Tag 3', author=up3, snapshot=s1)
        t21 = Tag.objects.create( text = 'Random Tag 1', author=up1, snapshot=s1)
        t22 = Tag.objects.create( text = 'Random Tag 2', author=up2, snapshot=s1)
        t23 = Tag.objects.create( text = 'Random Tag 3', author=up3, snapshot=s2)
        t31 = Tag.objects.create( text = 'Random Tag 1', author=up1,snapshot=s2)
        t32 = Tag.objects.create( text = 'Random Tag 2', author=up2,snapshot=s2)
        t33 = Tag.objects.create( text = 'Random Tag 3', author=up3,snapshot=s2)

        print(Fore.GREEN+"4.11.INSERT CHATS")
        c1 = Chat.objects.create( user1 = up1, user2 = up2)
        c2 = Chat.objects.create( user1 = up1, user2 = up3)

        print(Fore.GREEN+"4.10.INSERT MESSAGE")
        m1  = Message.objects.create( sender = up1, receiver = up2 , text = "Hello, how are you?", chat = c1, timestamp = timezone.make_aware( datetime.now() ))
        m2  = Message.objects.create( sender = up2, receiver = up1,  text = "I am fine, thank you!", chat = c1, timestamp = timezone.make_aware( datetime.now() ))
        m3  = Message.objects.create( sender = up1, receiver = up3 , text = "Hi User3, let´s met at 8PM ok?", chat = c2, timestamp = timezone.make_aware( datetime.now() ))
        

        print(Fore.GREEN+"4.11.INSERT UPVOTES")
        uv1 = Upvote.objects.create(upvoter=up1, type=1, tag=None, comment=None, snapshot=s1)
        uv2 = Upvote.objects.create(upvoter=up2, type=1, tag=None, comment=None, snapshot=s1)

        print (Fore.GREEN+"4.12.INSERT FOLLOWS")
        f1 = Follow.objects.create(follower=up1, stalker=up2)
        f2 = Follow.objects.create(follower=up2, stalker=up1)
        f3 = Follow.objects.create(follower=up1, stalker=up3)


        #if and_option == 'run':
         #   call_command('runserver')

        
