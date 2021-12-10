# Generated by Django 3.0.14 on 2021-12-10 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BV_MediaUploadResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BV_PostMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MediaImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_x', models.IntegerField()),
                ('img_y', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MediaVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SnapShotMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(default='', max_length=50)),
                ('media_access_token', models.CharField(default='', max_length=50, unique=True)),
                ('media_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media_image', to='media.MediaImage')),
                ('media_video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media_video', to='media.MediaVideo')),
                ('snapshot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='media', to='post.Snapshot')),
            ],
        ),
    ]
