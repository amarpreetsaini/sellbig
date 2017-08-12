from django import forms
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.aggregates import Max
from django.template import RequestContext

from feed.models import Feed, Activity

from account.models import User_info, Business
from account.views import custom_wall_post

from talks.models import Talk, Talk_comment, Comment_vote
from talks.forms import AddTalkForm, AddCommentForm

from endless_pagination.decorators import page_template

import json as simplejson
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils.timezone import utc

@login_required
@page_template('talks_feed.html')
def add_talk(request, template='talks.html', extra_context=None):
	data = {}
	if extra_context is not None:
		data.update(extra_context)
		
	user_info_obj = User_info.objects.get(user_id=request.user)
	talk_form = AddTalkForm()
	if request.method == 'POST' and request.is_ajax:
		talk_form = AddTalkForm(request.POST)
		if talk_form.is_valid() and request.POST['talk-cat'] and request.POST['sub-cat']:
			cd = talk_form.cleaned_data
			m_tags = talk_form.cleaned_data['m_tags']
			#user_info_obj = User_info.objects.get(user_id=request.user)
			slug = slugify(cd['title'])[0:70]
			
			cat_obj = Category.objects.get(id=request.POST['talk-cat'])
			sub_obj = Subcategory.objects.get(id=request.POST['sub-cat'])
			
			""" Check to determine whether user or business is starting a talk """
			if not request.session.get('business'):
				biz_check = 0
			elif request.session.get('business') == 1:
				biz_check = 1
			elif request.session.get('business') == 0:
				biz_check = 0
			
			if biz_check == 1:
				business_obj = Business.objects.get(user=request.user.id)
				talk = Talk.objects.create(business=business_obj, title=(cd['title'])[0:150], description=(cd['description'])[0:1000], category=cat_obj, subcategory=sub_obj)
				#comment_obj = Talk_comment.objects.create(business=business_obj, talk=talk, comment=cd['comment'])
				feed_obj = Feed.objects.create(business=business_obj, talk=talk, feed_type='T')
			elif biz_check == 0:
				talk = Talk.objects.create(user=user_info_obj, title=(cd['title'])[0:150], description=(cd['description'])[0:1000], category=cat_obj, subcategory=sub_obj)
				#comment_obj = Talk_comment.objects.create(user=user_info_obj, talk=talk, comment=cd['comment'])	
				feed_obj = Feed.objects.create(user=user_info_obj, talk=talk, feed_type='T')
			
			# to be removed as we have added cat and sub cat
			if request.POST.getlist('talk-chk[]'):
				for chkbox in request.POST.getlist('talk-chk[]'):
					m_tags.insert(0,chkbox)
			for tag in m_tags:
				talk.tags.add(tag.lower())
			#talk.tags.add(*m_tags)
			slug = slug + '-' + str(talk.id)
			talk.slug = slug
			talk.save()
			
			""" Check whether checkbox to post to Facebook is checked or not """
			if 'fb-chk' in request.POST:
				link = "/talks/"+slug+"/"
				custom_wall_post(request, link)
				
			talk_form = AddTalkForm()
			talk_obj = Talk.objects.filter(status='A').order_by("-added")
			return HttpResponseRedirect("/talks/"+slug+"/")
			#return render_to_response("talks_div.html", { 'talk': talk}, context_instance=RequestContext(request))
		#return HttpResponse(simplejson.dumps(talk_obj), mimetype="application/json")
	else:
		talk_form = AddTalkForm()
	talk_obj = Talk.objects.filter(status='A').order_by("-added")
	
	""" new talk object for trending talks """
	last_week = datetime.utcnow().replace(tzinfo=utc) - timedelta(days=7)
	trending_talks_obj = Talk.objects.filter(added__gte=last_week).order_by('-comments_count','-added')[:3]

	""" Notification code commented, added in context processors """
	"""
	id_list = Talk_comment.objects.filter(user=user_info_obj).values('user','talk').annotate(Max('id')).values('id__max')
	#notify_obj = Talk_comment.objects.filter(user=user_info_obj).values('user','talk').annotate(Max('id'))
	notify_obj = Talk_comment.objects.filter(pk__in=id_list).exclude(notify_count=0)
	"""
	
	data['talk_form'] = talk_form
	data['talk_obj'] = talk_obj
	data['trending_talks_obj'] = trending_talks_obj
	return render_to_response(template, data, context_instance=RequestContext(request))
	#return render(request, "talks.html", {
	#		'form': form, 'talk_obj': talk_obj, #'notify_obj': notify_obj
	#	})

@login_required
@page_template('talk_comment_feed.html')
def talk_comment(request, slug, template='talk_comment.html', extra_context=None):
	data = {}
	if extra_context is not None:
		data.update(extra_context)
	
	talk_obj = get_object_or_404(Talk, slug=slug)
	user_info_obj = User_info.objects.get(user_id=request.user)
	form = AddCommentForm()
	if request.method == 'POST' and request.is_ajax:
		print 'in POST'
		l_comments_count = talk_obj.comments_count
		form = AddCommentForm(request.POST)
		try:
			Feed.objects.get(user_id=user_info_obj, talk_id=talk_obj)
		except Feed.DoesNotExist:
			feed_check = True
		except Feed.MultipleObjectsReturned:
			feed_check = False
		else:
			feed_check = False
			
		""" Check to determine whether user or business is starting a talk """
		if not request.session.get('business'):
			biz_check = 0
		elif request.session.get('business') == 1:
			biz_check = 1
		elif request.session.get('business') == 0:
				biz_check = 0
			
		if 'parent' in request.POST:
			if form.is_valid():
				cd = form.cleaned_data
				if not len(cd['comment']) == 0:
					if biz_check == 1:
						business_obj = Business.objects.get(user=request.user.id)
						comment = Talk_comment.objects.create(business=business_obj, talk=talk_obj, comment=(cd['comment'])[0:500])	
						talk_obj.comments_count = l_comments_count + 1
						if feed_check:
							feed_obj = Feed.objects.create(business=business_obj, talk=talk_obj, comment=comment, feed_type='TC')
						activity_obj = Activity.objects.create(business=business_obj, comment=comment, activity_type='C')
					else:
						Talk_comment.objects.filter(talk=talk_obj).update(notify_count=F('notify_count')+1)
						comment = Talk_comment.objects.create(user=user_info_obj, talk=talk_obj, comment=(cd['comment'])[0:500])	
						talk_obj.comments_count = l_comments_count + 1
						if feed_check:
							feed_obj = Feed.objects.create(user=user_info_obj, talk=talk_obj, comment=comment, feed_type='TC')
						activity_obj = Activity.objects.create(user=user_info_obj, comment=comment, activity_type='C')
					talk_obj.save()
					return render_to_response("talk_comment_div.html", { 'comment': comment, 'form': form}, context_instance=RequestContext(request))

		elif 'child' in request.POST:
			print 'in child'
			if form.is_valid():
				print 'in form'
				cd = form.cleaned_data
				if not len(cd['comment']) == 0:
					if biz_check == 1:
						if Talk_comment.objects.filter(id=request.POST['parent_id']).exists():
							business_obj = Business.objects.get(user=request.user.id)
							parent = Talk_comment.objects.get(id=request.POST['parent_id'])
							comment = Talk_comment.objects.create(business=business_obj, talk=talk_obj, parent=parent, comment=(cd['comment'])[0:500])
							talk_obj.comments_count = l_comments_count + 1
							if feed_check:
								feed_obj = Feed.objects.create(business=business_obj, talk=talk_obj, comment=comment, feed_type='TC')
							activity_obj = Activity.objects.create(business=business_obj, comment=comment, activity_type='C')
						else:
							raise Http404
					else:
						if Talk_comment.objects.filter(id=request.POST['parent_id']).exists():
							parent = Talk_comment.objects.get(id=request.POST['parent_id'])
							comment = Talk_comment.objects.create(user=user_info_obj, talk=talk_obj, parent=parent, comment=(cd['comment'])[0:500])
							talk_obj.comments_count = l_comments_count + 1
							if feed_check:
								feed_obj = Feed.objects.create(user=user_info_obj, talk=talk_obj, comment=comment, feed_type='TC')
							activity_obj = Activity.objects.create(user=user_info_obj, comment=comment, activity_type='C')
						else:
							raise Http404
					talk_obj.save()
					return render_to_response("talk_comment_reply_div.html", { 'reply': comment, 'form': form}, context_instance=RequestContext(request))
	
		elif 'delete' in request.POST:
			if form.is_valid():
				cd = form.cleaned_data
				comment_del = Talk_comment.objects.get(id=request.POST['comment_id'])
				
				""" logic to cout the number of child comments to be deleted """
				delete_count = 0
				if comment_del.parent is None:
					delete_count = Talk_comment.objects.filter(parent=request.POST['comment_id']).count()
	
				comment_del.delete()
				talk_obj.comments_count = l_comments_count - 1 - delete_count
				#return HttpResponseRedirect("")
		elif 'up' in request.POST:
			if Talk_comment.objects.filter(id=request.POST['comment_id']).exists():
				comment_up = Talk_comment.objects.get(id=request.POST['comment_id'])
				
				if biz_check == 1:
					business_obj = Business.objects.get(user=request.user.id)
					if Comment_vote.objects.filter(business=business_obj, talk_comment=comment_up).exists():
						""" will add messages framework here """
						#return HttpResponseRedirect("")
					else:
						vote_obj = Comment_vote.objects.create(business=business_obj, talk=comment_up, vote_type='U')
						comment_up.up_count += 1
						comment_up.save()
				else:
					if Comment_vote.objects.filter(user=user_info_obj, talk_comment=comment_up).exists():
						""" will add messages framework here """
						#return HttpResponseRedirect("")
					else:
						vote_obj = Comment_vote.objects.create(user=user_info_obj, talk_comment=comment_up, vote_type='U')
						comment_up.up_count += 1
						comment_up.save()
				return HttpResponse(simplejson.dumps(comment_up.up_count-comment_up.down_count), mimetype="application/json")
				#return render_to_response("talk_comment_div.html", { 'comment': comment, 'form': form}, context_instance=RequestContext(request))
			else:
				raise Http404
		elif 'down' in request.POST:
			if Talk_comment.objects.filter(id=request.POST['comment_id']).exists():
				comment_down = Talk_comment.objects.get(id=request.POST['comment_id'])
				
				if biz_check == 1:
					business_obj = Business.objects.get(user=request.user.id)
					if Comment_vote.objects.filter(business=business_obj, talk_comment=comment_down).exists():
						""" will add messages framework here """
						#return HttpResponseRedirect("")
					else:
						vote_obj = Comment_vote.objects.create(business=business_obj, talk=comment_down, vote_type='D')
						comment_down.down_count += 1
						comment_down.save()
				else:
					if Comment_vote.objects.filter(user=user_info_obj, talk_comment=comment_down).exists():
						""" will add messages framework here """
						#return HttpResponseRedirect("")
					else:
						vote_obj = Comment_vote.objects.create(user=user_info_obj, talk_comment=comment_down, vote_type='D')
						comment_down.down_count += 1
						comment_down.save()
				return HttpResponse(simplejson.dumps(comment_down.up_count-comment_down.down_count), mimetype="application/json")
			else:
				raise Http404
		
		talk_obj.save()
		
		return HttpResponseRedirect("")
	else:
		form = AddCommentForm()

	comment_obj = Talk_comment.objects.filter(talk=talk_obj).filter(parent__isnull=True).order_by("-added")

	data['form'] = form
	data['talk_obj'] = talk_obj
	data['comment_obj'] = comment_obj
	return render_to_response(template, data, context_instance=RequestContext(request))
	#return render(request, "talk_comment.html", {
	#		'form': form, 'talk_obj': talk_obj, 'comment_obj': comment_obj,
	#	})
