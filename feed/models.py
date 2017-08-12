from django.db import models
from account.models import User_info, Business, Business_users, Category, Subcategory
from talks.models import Talk, Talk_comment
from taggit.managers import TaggableManager
from friends.models import Friendship
from taggit.models import Tag
from cities.models import City

class Wish(models.Model):
	user = models.ForeignKey(User_info)
	wish_text = models.CharField(max_length=150)
	desc = models.CharField(max_length=500, null=True)
	price = models.IntegerField(max_length=10, null=True)
	status = models.CharField(max_length=1, default='A')
	rewish_count = models.IntegerField(max_length=10, default=0)
	slug = models.SlugField(max_length=100, null=True)
	category = models.ForeignKey(Category, null=True)
	subcategory = models.ForeignKey(Subcategory, null=True)
	wish_type = models.CharField(max_length=5, null=True)
	location = models.ForeignKey(City, null=True)
	whatsapp_chk = models.BooleanField(default=False)
	contact = models.BigIntegerField(blank=True, null=True)
	added = models.DateTimeField(auto_now_add=True)
	tags = TaggableManager(blank=True)

class Wish_image(models.Model):
	wish = models.ForeignKey(Wish)
	image = models.ImageField(upload_to='wish_images', null=True, blank=True)
	status = models.CharField(max_length=2, default='A')
	added = models.DateTimeField(auto_now_add=True)

class Billboard(models.Model):
	business = models.ForeignKey(Business)
	billboard = models.ImageField(upload_to='billboards', default='billboards/default.jpeg', null=True, blank=True)
	status = models.CharField(max_length=1, default='A')
	added = models.DateTimeField(auto_now_add=True)

class Rating_tag(models.Model):
	tag = models.ForeignKey(Tag)
	rating = models.IntegerField(max_length=10)
	count = models.IntegerField(max_length=10)

	def __unicode__(self):
		return self.count

class Rating_owned(models.Model):
	rating_tag = models.ForeignKey(Rating_tag)
	user = models.ForeignKey(User_info)
	rating = models.IntegerField(max_length=1)
	owned_type = models.CharField(max_length=2, default='O')
	added = models.DateTimeField(auto_now_add=True)

class Feed(models.Model):
	user = models.ForeignKey(User_info, null=True)
	business = models.ForeignKey(Business, null=True)
	wish = models.ForeignKey(Wish, null=True)
	billboard = models.ForeignKey(Billboard, null=True)
	rating = models.ForeignKey(Rating_owned, null=True)
	talk = models.ForeignKey(Talk, null=True)
	comment = models.ForeignKey(Talk_comment, null=True)
	feed_type = models.CharField(max_length=2)
	status = models.CharField(max_length=1, default='A')
	added = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
	user = models.ForeignKey(User_info, null=True)
	business = models.ForeignKey(Business, null=True)
	friend_added = models.ForeignKey(Friendship, null=True)
	business_added = models.ForeignKey(Business_users, null=True)
	comment = models.ForeignKey(Talk_comment, null=True)
	activity_type = models.CharField(max_length=2)
	status = models.CharField(max_length=1, default='A')
	added = models.DateTimeField(auto_now_add=True)
