from feed.models import Feed, Wish
from account.models import User_info, Category
from talks.models import Talk_comment
from friends.models import FriendshipInvitation

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models.aggregates import Max

def notifications(request):
	print request.method
	
	user_info_obj = User_info.objects.filter(user_id=request.user.id)
	
	#wish notification
	wish_id_list = Wish.objects.filter(user=user_info_obj).values('id')
	rewish_count_obj = Feed.objects.filter(wish__in=wish_id_list).filter(status='A', feed_type='RW').exclude(user=user_info_obj).order_by("-added")
	
	#talk notification
	id_list = Talk_comment.objects.filter(user=user_info_obj).values('user','talk').annotate(Max('id')).values('id__max')
	talk_count_obj = Talk_comment.objects.filter(pk__in=id_list).exclude(notify_count=0)
	
	#friend requests received
	invitations = FriendshipInvitation.objects.filter(to_user=request.user.id).order_by("-sent")
	
	notify_count = rewish_count_obj.count() + talk_count_obj.count() + invitations.count()
	
	#to get categories and sub categories in filters
	cat_obj = Category.objects.filter(status='A')
	
	return ({'notify_count': notify_count, 'cat_obj': cat_obj})
