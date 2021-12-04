from core.models import  Upvote, UserProfile, Comment, Follow,Snapshot, Message, Tag
from post.models import MediaImage, MediaVideo, SnapShotMedia, Location
from user.models import UserImage
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.core.management import call_command
from django.contrib.auth.models import User
from colorama import init, Fore, Back, Style
from pathlib import Path
import shutil
import os

class Command(BaseCommand):

    help = 'Inserts dummy records'

    def add_argument(self, parser):
        pass
        #parser.add_argument('')
    def handle(self, *args, **options):
        
        init(autoreset=True)

        #cursor = connection.cursor()

        #1. Delete all Tables

        #print(Fore.GREEN+"1.DROP TABLES")
        #cursor.execute('DROP TABLE IF EXISTS core_location')
        ##print(Fore.GREEN+"1.DROP TABLES")
        #cursor.execute('DROP TABLE IF EXISTS core_userprofile')
        ##print(Fore.GREEN+"1.DROP TABLES")
        #cursor.execute('DROP TABLE IF EXISTS core_comment')
        #cursor.execute('DROP TABLE IF EXISTS core_tag')
        #cursor.execute('DROP TABLE IF EXISTS core_follow')
        #cursor.execute('DROP TABLE IF EXISTS core_snapshot')
        #cursor.execute('DROP TABLE IF EXISTS core_message')
        #cursor.execute('DROP TABLE IF EXISTS core_userimage')
        #cursor.execute('DROP TABLE IF EXISTS core_snapshotimage')

        #User.objects.all().delete()
        #cursor.execute('DELETE FROM auth_user WHERE 1 = 1')
        
        #2. Delete all migration entries in db
        #print(Fore.GREEN+"2.DELETE MIGRATIONS IN DB")
        #cursor.execute('DELETE FROM django_migrations WHERE app = "core"')
        
        #1-2. DROP DATABASE
        print(Fore.GREEN+"1-2.DROP DATABASE")
        if os.path.exists("db.sqlite3"):
            os.system('del db.sqlite3')
            #exec("rm db.sqlite3")

        #3. Remove all migrations from fs
        print(Fore.GREEN+"3.DELETE MIGRATIONS ON FS")
        if Path('core/migrations').exists():
            shutil.rmtree('core/migrations')
        os.mkdir('core/migrations')

        open('core/migrations/__init__.py','w').close()


        #4. Create Initial Migration
        print(Fore.GREEN+"4.RUN MIGRATIONS")
        call_command('makemigrations')
        call_command('migrate')

        #5 Population Database with new Data
#Location, UserProfile, Comment, Follow,Snapshot, Message, Tag, UserImage

        print(Fore.GREEN+"4.POPULATE DB")
        print(Fore.GREEN+"4.1.INSERT USER")
        admin = User.objects.create_user(username='admin', password='admin', is_superuser=True)
        u1 = User.objects.create_user(username='user1', password='password1')
        u2 = User.objects.create_user(username='user2', password='password2')
        u3 = User.objects.create_user(username='user3', password='password3')

        print(Fore.GREEN+"4.2.INSERT USERIMAGE")
        ui1 = UserImage.objects.create( filename = 'file1',  filetype = 'jpg',  img_x = 100,  img_y = 100 )
        ui2 = UserImage.objects.create( filename = 'file2',  filetype = 'jpg',  img_x = 100,  img_y = 100 )
        ui3 = UserImage.objects.create( filename = 'file3',  filetype = 'jpg',  img_x = 100,  img_y = 100 )

        print(Fore.GREEN+"4.3.INSERT USERPROFILE")
        up1 = UserProfile.objects.create(user = u1, username='user1', firstname='Firstname1', lastname='lastname1', pic = ui1)
        up2 = UserProfile.objects.create(user = u2, username='user2', firstname='Firstname2', lastname='lastname2', pic = ui2)
        up3 = UserProfile.objects.create(user = u3, username='user3', firstname='Firstname3', lastname='lastname3', pic = ui3)
      
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

        print(Fore.GREEN+"4.5.3 INSERT SNAPSHOTMEDIA")
        sm1 = SnapShotMedia.objects.create( media_type = 1, media_url='www.google.de', media_filetype='png', media_image=mi1, media_video=None)
        sm2 = SnapShotMedia.objects.create( media_type = 1, media_url='www.google.de', media_filetype='png', media_image=mi2, media_video=None)
        sm3 = SnapShotMedia.objects.create( media_type = 2, media_url='www.google.de', media_filetype='png', media_image=None, media_video=mv1)

        print(Fore.GREEN+"4.6.INSERT SNAPSHOT")
        s1 = Snapshot.objects.create( title = 'Snapshot1' , description = 'This is Snapshot 1', author = up1, media = sm1, location = l1, upvotes =101)
        s2 = Snapshot.objects.create( title = 'Snapshot2' , description = 'This is Snapshot 2', author = up1, media = sm2, location = l2, upvotes =102)
        s3 = Snapshot.objects.create( title = 'Snapshot3' , description = 'This is Snapshot 3', author = up1, media = sm3, location = l3, upvotes =103)

        print(Fore.GREEN+"4.7.INSERT COMMENT")
        c11 = Comment.objects.create( text = 'Random Comment 1', snapshot=s1,  author=up1, upvotes=1)
        c12 = Comment.objects.create( text = 'Random Comment 2', snapshot=s2,  author=up2, upvotes=2)
        c13 = Comment.objects.create( text = 'Random Comment 3', snapshot=s3,  author=up3, upvotes=3)
        c21 = Comment.objects.create( text = 'Random Comment 1', snapshot=s1,  author=up1, upvotes=1)
        c22 = Comment.objects.create( text = 'Random Comment 2', snapshot=s2,  author=up2, upvotes=2)
        c23 = Comment.objects.create( text = 'Random Comment 3', snapshot=s3,  author=up3, upvotes=3)
        c31 = Comment.objects.create( text = 'Random Comment 1', snapshot=s1,  author=up1, upvotes=1)
        c32 = Comment.objects.create( text = 'Random Comment 2', snapshot=s2,  author=up2, upvotes=2)
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

        print(Fore.GREEN+"4.9.INSERT MESSAGE")
        m1  = Message.objects.create( sender = up1, receiver = up2 , text = "Hello User 2, I am 1")
        m2  = Message.objects.create( sender = up1, receiver = up3,  text = "Hello User 3, I am 1")

        print(Fore.GREEN+"4.9.INSERT UPVOTES")
        uv1 = Upvote.objects.create(upvoter=up1, type=1, tag=None, comment=None, snapshot=s1)
        uv2 = Upvote.objects.create(upvoter=up2, type=1, tag=None, comment=None, snapshot=s1)

        print (Fore.GREEN+"4.10.INSERT FOLLOWS")
        f1 = Follow.objects.create(follower=up1, stalker=up2)
        f2 = Follow.objects.create(follower=up2, stalker=up1)
        f3 = Follow.objects.create(follower=up1, stalker=up3)

#upvoter = models.ForeignKey(UserProfile, on_delete=SET_NULL, related_name='upvoter', null=True)
#    type = models.IntegerField() #1 = tag, 2=comment, 3 = snapshot
#    tag = models.ForeignKey(Tag, on_delete=SET_NULL, related_name='tag_upvotes', null=True)
#    comment = models.ForeignKey(Comment, on_delete=SET_NULL, related_name='comment_upvotes', null=True)
#    snapshot



        #populate_db

        
