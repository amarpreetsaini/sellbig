# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
        ('account', '0002_auto_20151120_0027'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(max_length=2)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Billboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('billboard', models.ImageField(default=b'billboards/default.jpeg', null=True, upload_to=b'billboards', blank=True)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_type', models.CharField(max_length=2)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('billboard', models.ForeignKey(to='feed.Billboard', null=True)),
                ('business', models.ForeignKey(to='account.Business', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating_owned',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(max_length=1)),
                ('owned_type', models.CharField(default=b'O', max_length=2)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating_tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(max_length=10)),
                ('count', models.IntegerField(max_length=10)),
                ('tag', models.ForeignKey(to='taggit.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wish_text', models.CharField(max_length=150)),
                ('desc', models.CharField(max_length=500, null=True)),
                ('price', models.IntegerField(max_length=10, null=True)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('rewish_count', models.IntegerField(default=0, max_length=10)),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('wish_type', models.CharField(max_length=5, null=True)),
                ('whatsapp_chk', models.BooleanField(default=False)),
                ('contact', models.BigIntegerField(null=True, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(to='account.Category', null=True)),
                ('location', models.ForeignKey(to='cities.City', null=True)),
                ('subcategory', models.ForeignKey(to='account.Subcategory', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(to='account.User_info')),
            ],
        ),
        migrations.CreateModel(
            name='Wish_image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'wish_images', blank=True)),
                ('status', models.CharField(default=b'A', max_length=2)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('wish', models.ForeignKey(to='feed.Wish')),
            ],
        ),
        migrations.AddField(
            model_name='rating_owned',
            name='rating_tag',
            field=models.ForeignKey(to='feed.Rating_tag'),
        ),
        migrations.AddField(
            model_name='rating_owned',
            name='user',
            field=models.ForeignKey(to='account.User_info'),
        ),
    ]
