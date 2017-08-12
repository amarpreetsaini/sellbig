from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.aggregates import Max
from django.template import RequestContext
from django.contrib.auth import get_user_model

from endless_pagination.decorators import page_template

from messages.models import Thread, Message
from account.models import User_info
from account.decorators import is_profile
from messages.forms import SendMessageForm
from friends.models import Friendship

from datetime import datetime

@login_required
@is_profile
def send_message(request):
	
	#request.session['unread'] = 3
	#unread = request.session.get('unread')
	# in template folowing code
	# ({{ request.session.unread }})
	
	current_user = User_info.objects.get(user_id=request.user)
	friends = Friendship.objects.friends_for_user(request.user)
	friends_obj = User_info.objects.filter(user_id__in=friends)
	if request.method == 'POST':
		print 'message POST'
		form = SendMessageForm(request.POST)
		if form.is_valid():
			print 'form is valid'
			if 'send' in request.POST:
				print 'message send'
				cd = form.cleaned_data
				to_user_obj = User_info.objects.get(id=request.POST['to_user'])
				title = (cd['text'])[0:50]
				if 	Thread.objects.filter(Q(from_user=current_user, to_user=to_user_obj) | Q(from_user=to_user_obj, to_user=current_user)).exists():
					thread_obj = Thread.objects.get(Q(from_user=current_user, to_user=to_user_obj) | Q(from_user=to_user_obj, to_user=current_user))
					#thread_obj.from_title = title
					#thread_obj.to_title = title
					if thread_obj.from_user == current_user:
						thread_obj.to_title = title
						title = (cd['text'])[0:46]
						thread_obj.from_title = ('Me: ') + title
						thread_obj.to_unread += 1
					else:
						thread_obj.from_title = title
						title = (cd['text'])[0:46]
						thread_obj.to_title = ('Me: ') + title
						thread_obj.from_unread += 1
					thread_obj.from_status = 'A'
					thread_obj.to_status = 'A'
					thread_obj.added = datetime.now()
					thread_obj.save()
				else:
					from_title = ('Me: ') + (cd['text'])[0:46]
					thread_obj = Thread.objects.create(from_user=current_user, to_user=to_user_obj, from_title=from_title, to_title=title, to_unread=1)
				message_obj = Message.objects.create(thread=thread_obj, from_user=current_user, text=(cd['text'])[0:500])
				return HttpResponseRedirect("/messages/"+to_user_obj.user_id.username)
			elif 'delete' in request.POST:
				print 'message delete'
				thread_del = Thread.objects.get(id=request.POST['thread_id'])
				if thread_del.from_user == current_user:
					thread_del.from_status = 'D'
				else:
					thread_del.to_status = 'D'
				thread_del.save()
				
				""" for loop to make all messages of user in message table as D """
				for message_del in Message.objects.filter(thread=thread_del):
					if message_del.from_user == current_user:
						message_del.from_status = 'D'
					else:
						message_del.to_status = 'D'
					message_del.save()
				
				""" Check to delete from thread if both from and to status is 'D' """
				if thread_del.from_status == 'D' and thread_del.to_status == 'D':
					delete_message = Message.objects.filter(thread=thread_del)
					delete_message.delete()
					thread_del.delete()
			
			#return HttpResponseRedirect("/messages/")
	else:
		form = SendMessageForm()
	threads = Thread.objects.filter(Q(from_user=current_user) | Q(to_user=current_user)).exclude(Q(from_user=current_user, from_status='D') | Q(to_user=current_user, to_status='D')).order_by("-added")
	return render(request, "messages.html", {
			'form': form, 'threads': threads, 'friends_obj': friends_obj, 'current_user': current_user,
		})

@page_template('chat.html', 'chat')
@login_required
@is_profile
def message_chat(request, username, template='messages_chat.html', extra_context=None):
	print 'in message'
	data = {}
	if extra_context is not None:
		data.update(extra_context)
	
	current_user = User_info.objects.get(user_id=request.user)
	user_message = get_object_or_404(get_user_model(), username=username)
	to_user_obj = User_info.objects.get(user_id=user_message)	
	
	""" Main check for POST data """
	if request.method == 'POST':
		print 'chat POST'
		form = SendMessageForm(request.POST)
		if form.is_valid():
			
			""" Check to determine where new message is added or previous message is deleted """
			if 'send_msg' in request.POST:
				print 'chat send'
				cd = form.cleaned_data
				title = (cd['text'])[0:50]
				if 	Thread.objects.filter(Q(from_user=current_user, to_user=to_user_obj) | Q(from_user=to_user_obj, to_user=current_user)).exists():
					thread_obj = Thread.objects.get(Q(from_user=current_user, to_user=to_user_obj) | Q(from_user=to_user_obj, to_user=current_user))
					if thread_obj.from_user == current_user:
						thread_obj.to_title = title
						title = (cd['text'])[0:46]
						thread_obj.from_title = ('Me: ') + title
						thread_obj.to_unread += 1
					else:
						thread_obj.from_title = title
						title = (cd['text'])[0:46]
						thread_obj.to_title = ('Me: ') + title
						thread_obj.from_unread += 1
					thread_obj.to_status = 'A'
					thread_obj.from_status = 'A'
					thread_obj.added = datetime.now()
					thread_obj.save()
				else:
					thread_obj = Thread.objects.create(from_user=current_user, to_user=to_user_obj, from_title=title, to_title=title, to_unread=1)
				message_obj = Message.objects.create(thread=thread_obj, from_user=current_user, text=(cd['text'])[0:500])
				return render_to_response("messages_chat_div.html", { 'message_obj': message_obj, 'form': form}, context_instance=RequestContext(request))
			
			elif 'delete_msg' in request.POST:
				print 'chat delete'
				thread_del = Thread.objects.get(id=request.POST['thread_id'])
				message_del = Message.objects.get(id=request.POST['message_id'])
				
				""" check to find max_obj based on user in from_user or to_user """
				if message_del.from_user == current_user:
					max_before = Message.objects.filter(thread_id=thread_del).exclude(Q(from_user=current_user, from_status='D') | Q(~Q(from_user=current_user), to_status='D')).aggregate(Max('added'))['added__max']
					message_del.from_status = 'D'
					message_del.save()
					max_after = Message.objects.filter(thread_id=thread_del).exclude(Q(from_user=current_user, from_status='D') | Q(~Q(from_user=current_user), to_status='D')).aggregate(Max('added'))['added__max']
					
					""" check to determine whether after deleting a message, messages are there or not """
					if Message.objects.filter(added=max_after).exists():
						max_obj = Message.objects.get(added=max_after)
					else:
						max_obj = None
				else:
					max_before = Message.objects.filter(thread_id=thread_del).exclude(Q(from_user=current_user, from_status='D') | Q(~Q(from_user=current_user), to_status='D')).aggregate(Max('added'))['added__max']
					message_del.to_status = 'D'
					message_del.save()
					max_after = Message.objects.filter(thread_id=thread_del).exclude(Q(from_user=current_user, from_status='D') | Q(~Q(from_user=current_user), to_status='D')).aggregate(Max('added'))['added__max']
					if Message.objects.filter(added=max_after).exists():
						max_obj = Message.objects.get(added=max_after)
					else:
						max_obj = None
				
				if max_obj:
					del_title = (max_obj.text)
					if message_del.added == max_before:
						if thread_del.from_user == current_user:
							if max_obj.from_user == current_user:
								thread_del.from_title = ('Me: ') + (del_title)[0:46]
							else:
								thread_del.from_title = (del_title)[0:50]
						else:
							if max_obj.from_user == current_user:
								thread_del.to_title = ('Me: ') + (del_title)[0:46]
							else:
								thread_del.to_title = (del_title)[0:50]
						thread_del.save()
				else:
					if thread_del.from_user == current_user:
						thread_del.from_status = 'D'
						thread_del.save()
					else:
						thread_del.to_status = 'D'
						thread_del.save()
					
					""" Check to delete from thread if both from and to status is 'D' """
					if thread_del.from_status == 'D' and thread_del.to_status == 'D':
						delete_message = Message.objects.filter(thread=thread_del)
						delete_message.delete()
						thread_del.delete()
				
				""" Check to delete from message if both from and to status is 'D'"""
				if message_del.from_status == 'D' and message_del.to_status == 'D':
					message_del.delete()
			return HttpResponseRedirect("")
	else:
		form = SendMessageForm()
	
	""" Check to redirect to messages if all mesages in thread got deleted """
	if Thread.objects.filter(Q(from_user=current_user, to_user=to_user_obj) | Q(from_user=to_user_obj, to_user=current_user)).exists():
		print "thread if"
		chat_thread = Thread.objects.get(Q(from_user=current_user, to_user=to_user_obj) | Q(from_user=to_user_obj, to_user=current_user))
		# dont know why this condition??
		#if (chat_thread.from_user == current_user and chat_thread.from_status == 'D') or (chat_thread.to_user == current_user and chat_thread.to_status == 'D'):
		#	return HttpResponseRedirect("/messages")

		""" Check for marking unread messages as read on viewing the messages """
		if chat_thread.from_user == current_user:
			chat_thread.from_unread = 0
		else:
			chat_thread.to_unread = 0
		chat_thread.save()
		
		messages = Message.objects.filter(thread=chat_thread).exclude(Q(from_user=current_user, from_status='D') | Q(~Q(from_user=current_user), to_status='D')).order_by("-added")
		data['messages'] = messages
		
	else:
		print "thread else"
		return HttpResponseRedirect("/messages")

	
	
	data['form'] = form
	data['current_user'] = current_user
	data['user_message'] = user_message
	return render_to_response(template, data, context_instance=RequestContext(request))
