from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save

from django_facebook.signals import facebook_post_update

from cities.models import City

from taggit.managers import TaggableManager
from taggit.models import Tag

from sorl.thumbnail import ImageField

from account.managers import Business_usersManager

gender_choices = (
    ('M',u'Male'),
    ('F',u'Female'),
    )

class User_info(models.Model):
	user_id = models.OneToOneField(settings.AUTH_USER_MODEL)
	dob = models.DateField(blank=True, null=True) # not used
	gender = models.CharField(max_length=15,choices=gender_choices, blank=True, null=True) # not used
	city = models.CharField(max_length=50, blank=True, null=True) # not used
	state = models.CharField(max_length=50, blank=True, null=True) # not used
	country = models.CharField(max_length=50, blank=True, null=True) # not used
	company = models.CharField(max_length=100, blank=True, null=True)
	education1 = models.CharField(max_length=200, blank=True, null=True)
	education2 = models.CharField(max_length=200, blank=True, null=True)
	education3 = models.CharField(max_length=200, blank=True, null=True)	
	location = models.ForeignKey(City, null=True)
	contact = models.BigIntegerField(blank=True, null=True)
	avatar = models.ImageField(upload_to='user_images', default='user_images/root.jpeg', null=True, blank=True, max_length=255)
	about_tags = TaggableManager(blank=True)

class Business(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150,blank=True)
	official_tag = models.CharField(max_length=50, unique=True)
	city = models.CharField(max_length=50, blank=True, null=True)
	state = models.CharField(max_length=50, blank=True, null=True)
	country = models.CharField(max_length=50, blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	contact = models.IntegerField(max_length=20, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	website = models.URLField(blank=True, null=True)
	start_date = models.DateField(blank=True, null=True)
	member_count = models.IntegerField(max_length=20, blank=True, null=True)
	visit_count = models.IntegerField(max_length=20, blank=True, null=True)
	logo = models.ImageField(upload_to='business_logo', default='business_logo/default/biz_default.jpeg', null=True, blank=True)
	tags = TaggableManager(blank=True)
	
	def __unicode__(self):
		return self.name

class Business_users(models.Model):
	business = models.ForeignKey(Business)
	user = models.ForeignKey(User_info)
	added = models.DateTimeField(auto_now_add=True)
	
	objects = Business_usersManager()

	def __unicode__(self):
		return self.business.name
		
	def type(self):
		return 'B'

class Category(models.Model):
	name = models.CharField(max_length=150)
	status = models.CharField(max_length=1, default='A')
	count = models.IntegerField(max_length=10, default=0)
	added = models.DateTimeField(auto_now_add=True)
	
	# added to display category name while ading sub-cat in django admin
	# and to return name in search filters
	def __unicode__(self):
		return self.name

class Subcategory(models.Model):
	name = models.CharField(max_length=150)
	status = models.CharField(max_length=1, default='A')
	category = models.ForeignKey(Category)
	count = models.IntegerField(max_length=10, default=0)
	added = models.DateTimeField(auto_now_add=True)

	# added to display category name while ading sub-cat in django admin
	# and to return name in search filters
	def __unicode__(self):
		return self.name
	
	class Meta:
		ordering = ['added']

def business_exists(sender, user, request, **kwargs):
	if Business.objects.filter(user=request.user.id).exists():
		request.session['business_exists'] = 1

user_logged_in.connect(business_exists)

def create_user_info(sender, instance, **kwargs):
	if kwargs['created']:
		try:
			User_info.objects.get(user_id=instance)
		except User_info.DoesNotExist:
			userinfo_obj = User_info(user_id=instance)
			userinfo_obj.save()
	
post_save.connect(create_user_info, sender=settings.AUTH_USER_MODEL)

def get_fb_image(sender, user, **kwargs):
	userinfo_obj = User_info.objects.get(user_id=user)
	userinfo_obj.avatar = user.image
	userinfo_obj.save()

facebook_post_update.connect(get_fb_image)
