# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='user_id',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(to='account.Category'),
        ),
        migrations.AddField(
            model_name='business_users',
            name='business',
            field=models.ForeignKey(to='account.Business'),
        ),
        migrations.AddField(
            model_name='business_users',
            name='user',
            field=models.ForeignKey(to='account.User_info'),
        ),
        migrations.AddField(
            model_name='business',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='business',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
