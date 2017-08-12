from django.db import models
from account.models import User_info, Business, Category, Subcategory
from taggit.managers import TaggableManager

class Talk(models.Model):
	user = models.ForeignKey(User_info, null=True)
	business = models.ForeignKey(Business, null=True)
	title = models.CharField(max_length=150)
	description = models.CharField(null=True, max_length=1000)
	category = models.ForeignKey(Category, null=True)
	subcategory = models.ForeignKey(Subcategory, null=True)
	slug = models.SlugField(max_length=100, null=True)
	comments_count = models.IntegerField(default=1)
	status = models.CharField(max_length=1, default='A')
	added = models.DateTimeField(auto_now_add=True)
	tags = TaggableManager(blank=True)

class Talk_comment(models.Model):
	user = models.ForeignKey(User_info, null=True)
	business = models.ForeignKey(Business, null=True)
	talk = models.ForeignKey(Talk)
	parent = models.ForeignKey('self', null=True, related_name='replies')
	comment = models.CharField(max_length=500)
	notify_count = models.IntegerField(default=0)
	up_count = models.IntegerField(default=0)
	down_count = models.IntegerField(default=0)
	status = models.CharField(max_length=1, default='A')
	added = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['added']

	def type(self):
		return 'C'

class Comment_vote(models.Model):
	user = models.ForeignKey(User_info, null=True)
	business = models.ForeignKey(Business, null=True)
	talk_comment = models.ForeignKey(Talk_comment)
	vote_type = models.CharField(max_length=2, null=True)
