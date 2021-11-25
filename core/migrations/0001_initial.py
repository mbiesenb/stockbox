# Generated by Django 3.2.9 on 2021-11-25 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(max_length=8)),
                ('latitude', models.CharField(max_length=8)),
                ('locationText', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=100)),
                ('upvotes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SnapShotImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=50)),
                ('filetype', models.CharField(max_length=10)),
                ('img_x', models.IntegerField()),
                ('img_y', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=50)),
                ('filetype', models.CharField(max_length=10)),
                ('img_x', models.IntegerField()),
                ('img_y', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('pic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.userimage')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=30)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.userprofile')),
                ('snapshot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tags', to='core.snapshot')),
            ],
        ),
        migrations.AddField(
            model_name='snapshot',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.userprofile'),
        ),
        migrations.AddField(
            model_name='snapshot',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.location'),
        ),
        migrations.AddField(
            model_name='snapshot',
            name='pic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.snapshotimage'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to='core.userprofile')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='follower', to='core.userprofile')),
                ('stalker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stalker', to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('upvotes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.userprofile')),
                ('snapshot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='core.snapshot')),
            ],
        ),
    ]
