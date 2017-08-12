# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('cities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150, blank=True)),
                ('official_tag', models.CharField(unique=True, max_length=50)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('contact', models.IntegerField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('member_count', models.IntegerField(max_length=20, null=True, blank=True)),
                ('visit_count', models.IntegerField(max_length=20, null=True, blank=True)),
                ('logo', models.ImageField(default=b'business_logo/default/biz_default.jpeg', null=True, upload_to=b'business_logo', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Business_users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('count', models.IntegerField(default=0, max_length=10)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('status', models.CharField(default=b'A', max_length=1)),
                ('count', models.IntegerField(default=0, max_length=10)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dob', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=15, null=True, choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('company', models.CharField(max_length=100, null=True, blank=True)),
                ('education1', models.CharField(max_length=200, null=True, blank=True)),
                ('education2', models.CharField(max_length=200, null=True, blank=True)),
                ('education3', models.CharField(max_length=200, null=True, blank=True)),
                ('contact', models.BigIntegerField(null=True, blank=True)),
                ('avatar', models.ImageField(default=b'user_images/root.jpeg', max_length=255, null=True, upload_to=b'user_images', blank=True)),
                ('about_tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('location', models.ForeignKey(to='cities.City', null=True)),
            ],
        ),
    ]
