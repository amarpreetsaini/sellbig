# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=500, null=True)),
                ('from_status', models.CharField(default=b'A', max_length=1)),
                ('to_status', models.CharField(default=b'A', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(to='account.User_info')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_title', models.CharField(max_length=50, null=True)),
                ('to_title', models.CharField(max_length=50, null=True)),
                ('from_unread', models.IntegerField(default=0, max_length=2)),
                ('to_unread', models.IntegerField(default=0, max_length=2)),
                ('from_status', models.CharField(default=b'A', max_length=1)),
                ('to_status', models.CharField(default=b'A', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(related_name='from_user', to='account.User_info')),
                ('to_user', models.ForeignKey(related_name='to_user', to='account.User_info')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='my_messages.Thread'),
        ),
    ]
