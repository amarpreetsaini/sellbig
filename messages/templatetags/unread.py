from django import template
from messages.models import Thread
from account.models import User_info
from django.db.models import Q

register = template.Library()

@register.filter
def unread_messages(user):
		count = 0
		#if not user.is_anonymous:
		user_obj = User_info.objects.get(user_id=user)
		unread_obj = Thread.objects.filter(Q(from_user=user_obj) | Q(to_user=user_obj)).exclude(Q(from_user=user_obj, from_status='D') | Q(to_user=user_obj, to_status='D'))
		for unread in unread_obj:
			if unread.from_user == user_obj:
				count += unread.from_unread
			elif unread.to_user == user_obj:
				count += unread.to_unread
		return count
		#else:
		#return count
