from django.db import models
from account.models import User_info

class Thread(models.Model):
	from_user = models.ForeignKey(User_info, related_name='from_user')
	to_user = models.ForeignKey(User_info, related_name='to_user')
	from_title = models.CharField(max_length=50, null=True)
	to_title = models.CharField(max_length=50, null=True)
	from_unread = models.IntegerField(max_length=2, default=0)
	to_unread = models.IntegerField(max_length=2, default=0)
	from_status = models.CharField(max_length=1, default='A')
	to_status = models.CharField(max_length=1, default='A')
	added = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
	thread = models.ForeignKey(Thread)
	from_user = models.ForeignKey(User_info)
	text = models.CharField(max_length=500, null=True)
	from_status = models.CharField(max_length=1, default='A')
	to_status = models.CharField(max_length=1, default='A')
	added = models.DateTimeField(auto_now_add=True)
