# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('account', '0002_auto_20151120_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment_vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_type', models.CharField(max_length=2, null=True)),
                ('business', models.ForeignKey(to='account.Business', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('comments_count', models.IntegerField(default=1)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(to='account.Business', null=True)),
                ('category', models.ForeignKey(to='account.Category', null=True)),
                ('subcategory', models.ForeignKey(to='account.Subcategory', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(to='account.User_info', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Talk_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=500)),
                ('notify_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(to='account.Business', null=True)),
                ('parent', models.ForeignKey(related_name='replies', to='talks.Talk_comment', null=True)),
                ('talk', models.ForeignKey(to='talks.Talk')),
                ('user', models.ForeignKey(to='account.User_info', null=True)),
            ],
            options={
                'ordering': ['added'],
            },
        ),
        migrations.AddField(
            model_name='comment_vote',
            name='talk_comment',
            field=models.ForeignKey(to='talks.Talk_comment'),
        ),
        migrations.AddField(
            model_name='comment_vote',
            name='user',
            field=models.ForeignKey(to='account.User_info', null=True),
        ),
    ]
