# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
        ('account', '0002_auto_20151120_0027'),
        ('talks', '0001_initial'),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='comment',
            field=models.ForeignKey(to='talks.Talk_comment', null=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='rating',
            field=models.ForeignKey(to='feed.Rating_owned', null=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='talk',
            field=models.ForeignKey(to='talks.Talk', null=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='user',
            field=models.ForeignKey(to='account.User_info', null=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='wish',
            field=models.ForeignKey(to='feed.Wish', null=True),
        ),
        migrations.AddField(
            model_name='billboard',
            name='business',
            field=models.ForeignKey(to='account.Business'),
        ),
        migrations.AddField(
            model_name='activity',
            name='business',
            field=models.ForeignKey(to='account.Business', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='business_added',
            field=models.ForeignKey(to='account.Business_users', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='comment',
            field=models.ForeignKey(to='talks.Talk_comment', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='friend_added',
            field=models.ForeignKey(to='friends.Friendship', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to='account.User_info', null=True),
        ),
    ]
