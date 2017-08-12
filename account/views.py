from django import forms
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Q
from django.db.models.aggregates import Max
from django.contrib.auth import get_user_model

from django_facebook.models import FacebookUser

from account.forms import RegisterForm, EditProfileForm, UserImageForm, AddBusinessForm, SettingsForm, LogoForm
from account.models import User_info, Business, Business_users
from account.decorators import is_profile, is_business

from feed.models import Wish, Feed, Billboard, Activity, Rating_owned, Rating_tag, Wish_image, Category
from feed.forms import AddWishForm

from talks.models import Talk_comment, Talk

from friends.models import Friendship, FriendshipInvitation

from taggit.models import Tag

from sorl.thumbnail import delete
from endless_pagination.decorators import page_template, page_templates
from itertools import chain
from operator import attrgetter
from datetime import datetime

import uuid

def newuser(request):
	return render(request, 'newuser.html')

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	else:
		if request.method == 'POST':
			form = RegisterForm(request.POST)
			if form.is_valid() and not request.POST['zipcode']:
				new_user = form.save()
				new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
				login(request, new_user)
				#new_user.gender = request.POST['gender-radio']
				#new_user.save()
				
				#userinfo_o = User_info(user_id=request.user)#, dob=request.POST['dob'], gender=request.POST['gender'],)
				#userinfo_o.save()

				request.session['new_user'] = 1
				newurl=request.POST['next']
				if newurl:
					return HttpResponseRedirect(newurl)
				else:
					return HttpResponseRedirect("/")
		else:
			form = RegisterForm()
		return render(request, "signup.html", {
			'form': form,
		})

@login_required
def add_business(request):
	""" Make new view for edit, remove edit code from this one """
	try:
		Business.objects.get(user_id=request.user.id)
	except Business.DoesNotExist:
		biz_check = False
	else:
		biz_check = True
	
	user_id = request.user.id
	if biz_check:
		inst = Business.objects.get(user_id=user_id)
	
	logo_form = LogoForm()
	if biz_check:
		form = AddBusinessForm(instance=inst)
	else:
		form = AddBusinessForm()
	
	if request.method == 'POST':
		if 'details' in request.POST:
			if biz_check:
				form = AddBusinessForm(request.POST, instance=inst)
			else:
				form = AddBusinessForm(request.POST)
			if form.is_valid():
				new_business = form.save(commit=False)
				new_business.user = request.user
				new_business.official_tag = (form.cleaned_data['official_tag']).lower()
				new_business.save()
				tags = form.cleaned_data['tags']
				tags.insert(0,form.cleaned_data['official_tag'])
				new_business.tags.clear()
				for tag in tags:
					new_business.tags.add(tag.lower())
				new_business.save()
				#new_business.tags.add(*tags)
				
				request.session['business_exists'] = 1
				request.session['business'] = 1
				
				#return HttpResponseRedirect("/office/")
		elif 'logo' in request.POST:
			logo_form = LogoForm(request.POST, request.FILES)
			if logo_form.is_valid():
				if 'logo' in request.FILES:
					logo_obj = Business.objects.get(user=request.user)
					logo_name = logo_obj.official_tag
					
					ext = request.FILES['logo'].content_type.split('/')[1]
					request.FILES['logo'].name = str(logo_name) + '.' + str(ext)
					
					if logo_obj.logo == 'business_logo/default/biz_default.jpeg':
						delete(logo_obj.logo, delete_file=False)
					else:
						delete(logo_obj.logo)
					
					logo_obj.logo = request.FILES['logo']
					logo_obj.save()
	
	return render(request, "add_business.html", {
		'form': form, 'logo_form': logo_form
	})

@login_required
@is_business
def add_logo(request):
	"""
	View to add logo to a business
	"""
	form = LogoForm()
	if request.method == 'POST':
            form = LogoForm(request.POST, request.FILES)
            if form.is_valid():
                if 'logo' in request.FILES:
					logo_obj = Business.objects.get(user=request.user)
					logo_name = logo_obj.official_tag
					
					ext = request.FILES['logo'].content_type.split('/')[1]
					request.FILES['logo'].name = str(logo_name) + '.' + str(ext)
					
					if logo_obj.logo == 'business_logo/default/biz_default.jpeg':
						delete(logo_obj.logo, delete_file=False)
					else:
						delete(logo_obj.logo)
					
					logo_obj.logo = request.FILES['logo']
					logo_obj.save()
                else:
					form = LogoForm()
	else:
            #form = LogoForm()
            return HttpResponseRedirect("/office")
	return render(request, "business_logo.html", {
        'form': form,
    })
	
@login_required
@is_business
@page_template('my_office_feed.html')
def my_office(request, template='my_office.html', extra_context=None):
	"""
	Visit page My Office
	"""
	#business = get_object_or_404(Business, user_id=request.user.id)
	data = {}
	if extra_context is not None:
		data.update(extra_context)
	
	try:
		business_obj = Business.objects.get(user_id=request.user.id)
	except Business.DoesNotExist:
		biz_check = True
	else:
		biz_check = False
		
	if biz_check:
		return add_business(request)
	else:
		if request.method == 'POST' and 'share' in request.POST:
			bb_obj = Billboard.objects.get(id=request.POST['billboard_id'])
			if Feed.objects.filter(business=business_obj, billboard=bb_obj).exists():
				feed_bb = Feed.objects.get(business=business_obj, billboard=bb_obj)
				added_feed = (feed_bb.added).replace(tzinfo=None)
				current_feed = datetime.now()
				diff_feed = current_feed - added_feed
				if diff_feed.days < 1:
					error_message = 'You have recently shared this billboard, come back after 24 hours'
				else:
					feed_bb.added = datetime.now()
					feed_bb.save()
			else:
				feed_obj = Feed.objects.create(business=business_obj, billboard=bb_obj, feed_type='SB')
			
		billboard = Billboard.objects.filter(business=business_obj).order_by('-added')
		biz_feed_obj = Feed.objects.filter(business=business_obj).filter(status='A').order_by("-added")
		biz_user_obj = Business_users.objects.filter(business=business_obj).order_by("-added")[:5]
		
		data['business'] = business_obj
		data['billboard'] = billboard
		data['biz_feed_obj'] = biz_feed_obj
		data['biz_user_obj'] = biz_user_obj
		
		return render_to_response(template, data, context_instance=RequestContext(request))
		#return render(request, 'my_office.html', {'business': business_obj, 'billboard': billboard, 'biz_feed_obj': biz_feed_obj, 'biz_user_obj': biz_user_obj})

@login_required	
@page_template('my_office_feed.html')
def business_detail(request, off_tag, template='business.html', extra_context=None):
	"""
	Visit business profile
	"""
	data = {}
	if extra_context is not None:
		data.update(extra_context)
    
	business = get_object_or_404(Business, official_tag=off_tag)
	billboard = Billboard.objects.filter(business=business).order_by('-added')
	user_obj = get_object_or_404(User_info, user_id=request.user)
	biz_feed_obj = Feed.objects.filter(business=business).filter(status='A').order_by("-added")
	biz_user_obj = Business_users.objects.filter(business=business).order_by("-added")[:5]
	
	#added = False
	#print added
	#if Business_users.objects.filter(business=business).filter(user=user_obj).exists():
	#	added = True
    
	if business.user == request.user:
		return HttpResponseRedirect("/office/")
	else:
		if request.method == 'POST':
			print 'business POST'
			if 'add' in request.POST:
				print 'business add'
				""" add check here as: only add new business_user if already not exists """
				business_user = Business_users(business=business, user=user_obj)
				business_user.save()
				activity_obj = Activity.objects.create(user=user_obj, business_added=business_user, activity_type='B')
			elif 'delete' in request.POST:
				print 'business delete'
				business_user = Business_users.objects.get(business=business, user=user_obj)
				business_user.delete()
			elif 'share' in request.POST:
				print 'business share'
				bb_obj = Billboard.objects.get(id=request.POST['billboard_id'])
				if Feed.objects.filter(user=user_obj, billboard=bb_obj).exists():
					feed_bb = Feed.objects.get(user=user_obj, billboard=bb_obj)
					added_feed = (feed_bb.added).replace(tzinfo=None)
					current_feed = datetime.now()
					diff_feed = current_feed - added_feed
					if diff_feed.days < 1:
						error_message = 'You have recently shared this billboard, come back after 24 hours'
					else:
						feed_bb.added = datetime.now()
						feed_bb.save()
				else:
					feed_obj = Feed.objects.create(user=user_obj, billboard=bb_obj, feed_type='SB')
		
		added = False
		if Business_users.objects.filter(business=business).filter(user=user_obj).exists():
			added = True
		
		data['business'] = business
		data['billboard'] = billboard
		data['added'] = added
		data['biz_feed_obj'] = biz_feed_obj
		data['biz_user_obj'] = biz_user_obj
		
		return render_to_response(template, data, context_instance=RequestContext(request))
		#return render(request, 'business.html', {'business': business, 'billboard': billboard, 'added': added, 'biz_feed_obj': biz_feed_obj, 'biz_user_obj': biz_user_obj})

@login_required
def business_contacts(request, off_tag):
	
	business = get_object_or_404(Business, official_tag=off_tag)
	biz_user_obj = Business_users.objects.filter(business=business).order_by("-added")
	
	return render(request, "business_contacts.html", {'biz_user_obj': biz_user_obj})

@login_required
@is_profile
def edit_profile(request):
	
	inst = User_info.objects.get(user_id=request.user)
	
	form = EditProfileForm(instance=inst)
	img_form = UserImageForm()
	
	if request.method == 'POST':
		"""if 'details' in request.POST:
			form = EditProfileForm(request.POST, instance=inst)
			if form.is_valid():
				edit_profile_obj = form.save(commit=False)
				about_tags = form.cleaned_data['about_tags']
				edit_profile_obj.about_tags.clear()
				for tag in about_tags:
					edit_profile_obj.about_tags.add(tag.lower())
				edit_profile_obj.save()
				if 'location' in request.POST and request.POST.get('location'):
					inst.location_id = request.POST.get('location')
					inst.save()
				#edit_profile_obj.about_tags.add(*about_tags)
				#return HttpResponseRedirect("/accounts/add_interest/")"""
		if 'location' in request.POST and request.POST.get('location'):
			inst.location_id = request.POST.get('location')
			inst.save()
		elif 'image' in request.POST:
			img_form = UserImageForm(request.POST, request.FILES)
			if img_form.is_valid():
				if 'avatar' in request.FILES:
					ext = request.FILES['avatar'].content_type.split('/')[1]
					request.FILES['avatar'].name = str(request.user) + '.' + str(ext)
					
					obj = User_info.objects.get(user_id=request.user)
					
					if obj.avatar == 'user_images/root.jpeg':
						delete(obj.avatar, delete_file=False)
					else:
						delete(obj.avatar)
					
					obj.avatar = request.FILES['avatar']
					obj.save()
                else:
					img_form = UserImageForm()
		return HttpResponseRedirect("/profile/")
	else:
		form = EditProfileForm(instance=inst)
		img_form = UserImageForm()
	return render(request, "edit_profile.html", {
        'form': form, 'img_form': img_form, 'user_obj': inst
    })

@page_template('profile_details_feed.html')
def profile_detail(request, username, template='profile_detail.html', extra_context=None):
	"""
	Visit profile of friend
	"""
	print 'in profile'
	data = {}
	if extra_context is not None:
		data.update(extra_context)
	
	profile = get_object_or_404(get_user_model(), username=username)
	profile_info = get_object_or_404(User_info, user_id_id=profile.id)
    
	businesses = Business_users.objects.filter(user=profile_info)[:7]
	
	friends_obj = Friendship.objects.friends_for_user(profile)
	myfriends = User_info.objects.filter(user_id__in=friends_obj)[:7]
	
	owned_obj = Rating_owned.objects.filter(user=profile_info).exclude(owned_type='O')
	
	wish_obj = Wish.objects.filter(user=profile_info).filter(status='A').order_by("-added")[:1]
	
	profile_feed_obj = Feed.objects.filter(user=profile_info).order_by("-added")
	
	is_friend = ''
	if request.user.is_authenticated():
		if Friendship.objects.are_friends(request.user, profile):
			is_friend = 'Y'
		else:
			previous_invitations_to = FriendshipInvitation.objects.filter(to_user=profile, from_user=request.user)
			previous_invitations_from = FriendshipInvitation.objects.filter(to_user=request.user, from_user=profile)
			if previous_invitations_to.count() > 0 or previous_invitations_from.count() > 0:
				is_friend = 'S'
			else:
				is_friend = 'N'

	if request.method == 'POST':
		common_feed_post(request)

	if profile == request.user:
		return HttpResponseRedirect("/profile/")
	else:
		data['profile_info'] = profile_info
		data['businesses'] = businesses
		data['myfriends'] = myfriends
		data['owned_obj'] = owned_obj
		data['wish_obj'] = wish_obj
		data['profile_feed_obj'] = profile_feed_obj
		data['is_friend'] = is_friend
		
		return render_to_response(template, data, context_instance=RequestContext(request))		
		#return render(request, 'profile_detail.html', {'profile_info': profile_info,'businesses': businesses,'myfriends': myfriends,'owned_obj': owned_obj,'wish_obj': wish_obj,'profile_feed_obj': profile_feed_obj})

@login_required
def profile_contacts(request, username):
	
	profile = get_object_or_404(get_user_model(), username=username)
	profile_info = get_object_or_404(User_info, user_id_id=profile.id)
    
	businesses = Business_users.objects.filter(user=profile_info)
	
	friends_obj = Friendship.objects.friends_for_user(profile)
	myfriends = User_info.objects.filter(user_id__in=friends_obj)
	
	""" Find friends - doroko users that are facebook friends but not my friends """
	fb_list = FacebookUser.objects.filter(user_id=request.user.id).values('facebook_id')	
	friends_list = []
	# objects for my friends, to exclude
	my_friends = Friendship.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
	for friends in my_friends:
		if friends.from_user == request.user:
			friends_list.append(friends.to_user_id)
		else:
			friends_list.append(friends.from_user_id)
	# object for friend requests sent and received, to exclude
	my_invitations = FriendshipInvitation.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
	for invitations in my_invitations:
		if invitations.from_user == request.user:
			friends_list.append(invitations.to_user_id)
		else:
			friends_list.append(invitations.from_user_id)
	find_obj = get_user_model().objects.filter(facebook_id__in=fb_list).exclude(id__in=friends_list)#.values_list('username', 'first_name', 'last_name')
	
	""" Invite friends - facebook friends that are not doroko users """
	fb_id_list = []
	for friends in my_friends:
		if friends.from_user == request.user:
			if friends.to_user.facebook_id is not None:
				fb_id_list.append(friends.to_user.facebook_id)
		else:
			if friends.from_user.facebook_id is not None:
				fb_id_list.append(friends.from_user.facebook_id)
	invite_obj = FacebookUser.objects.filter(user_id=request.user.id).exclude(facebook_id__in=fb_id_list).values_list('facebook_id', 'name')
	
	return render(request, "profile_contacts.html",
							{
							'myfriends': myfriends,
							'businesses': businesses,
							'find_obj': find_obj,
							'invite_obj': list(invite_obj),
							'fb_id_list': fb_id_list,
							'username': username
							})

@login_required
def find_friends(request):
	term = request.GET.get('term') #jquery-ui.autocomplete parameter
    
	if term:
		fb_list = FacebookUser.objects.filter(user_id=request.user.id).values('facebook_id')	
		friends_list = []
		my_friends = Friendship.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
		for friends in my_friends:
			if friends.from_user == request.user:
				friends_list.append(friends.to_user_id)
			else:
				friends_list.append(friends.from_user_id)
		find_obj = get_user_model().objects.filter(Q(first_name__istartswith=term)|Q(last_name__istartswith=term)).filter(facebook_id__in=fb_list).exclude(id__in=friends_list).values_list('username', 'first_name', 'last_name')

		return HttpResponse(simplejson.dumps(find_obj))
	else:
		return HttpResponseRedirect("/")

@login_required
def invite_friends(request):
	term = request.GET.get('term') #jquery-ui.autocomplete parameter
    
	if term:
		fb_id_list = []
		my_friends = Friendship.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
		for friends in my_friends:
			if friends.from_user == request.user:
				if friends.to_user.facebook_id is not None:
					fb_id_list.append(friends.to_user.facebook_id)
			else:
				if friends.from_user.facebook_id is not None:
					fb_id_list.append(friends.from_user.facebook_id)
		invite_obj = FacebookUser.objects.filter(name__istartswith=term).filter(user_id=request.user.id).exclude(facebook_id__in=fb_id_list)#.values_list('facebook_id', 'name')
		invite_list = []
		for obj in invite_obj:
			file_info = {}
			file_info['label'] = obj.facebook_id
			file_info['value'] = obj.name
			invite_list.append(file_info)

		return HttpResponse(simplejson.dumps(invite_list))
	else:
		return HttpResponseRedirect("/")

@page_templates((('my_home_feed.html', None), ('my_home_activity.html', 'activity'),))
@login_required
@is_profile
def profile(request, template='my_home.html', extra_context=None):
	"""
	Visit page My Profile
	"""
	
	""" to reset session variable for signup flow of forms """
	if 'new_user' in request.session:
		del request.session['new_user']
	
	data = {}
	if extra_context is not None:
		data.update(extra_context)
		
	user_info = get_object_or_404(User_info, user_id_id=request.user.id)
	businesses = Business_users.objects.filter(user=user_info)[:7]
	
	friends_obj = Friendship.objects.friends_for_user(request.user)
	friends = User_info.objects.filter(user_id__in=friends_obj)[:7]
	
	owned_obj = Rating_owned.objects.filter(user=user_info).exclude(owned_type='O')
	
	wish_obj = Wish.objects.filter(user=user_info).filter(status='A').order_by("-added")[:1]
	
	user_feed_obj = Feed.objects.filter(user=user_info).order_by("-added")
	
	cat_obj = Category.objects.filter(status='A')
	
	print 'in my home'
	
	if request.method == 'POST':
		
		common_feed_post(request)
	
	data['user_info'] = user_info
	data['businesses'] = businesses
	data['friends'] = friends
	data['owned_obj'] = owned_obj
	data['user_feed_obj'] = user_feed_obj
	data['wish_obj'] = wish_obj
	data['cat_obj'] = cat_obj
	#data['wish_form'] = wish_form
	#data['activity_obj'] = activity_obj
	
	return render_to_response(template, data, context_instance=RequestContext(request))
	#return render(request, 'my_home.html', {'user_info': user_info, 'businesses': businesses, 'friends': friends, 'owned_obj': owned_obj, 'user_feed_obj': user_feed_obj, 'wish_form': wish_form})

@login_required
@is_profile
def user_image(request):
	form = UserImageForm()
	if request.method == 'POST':
            form = UserImageForm(request.POST, request.FILES)
            if form.is_valid():
                #name = request.FILES['profile_pic'].name
                if 'avatar' in request.FILES:
					ext = request.FILES['avatar'].content_type.split('/')[1]
					request.FILES['avatar'].name = str(request.user) + '.' + str(ext)
					
					obj = User_info.objects.get(user_id=request.user)
					
					if obj.avatar == 'user_images/root.jpeg':
						delete(obj.avatar, delete_file=False)
					else:
						delete(obj.avatar)
					
					obj.avatar = request.FILES['avatar']
					obj.save()
                else:
					form = UserImageForm()
					#obj = User_info.objects.create(user_id=request.user)
					#obj.save()
                
                #image = User_image(user=request.user, profile_pic=request.FILES['profile_pic'])
                #image.save()
                #image_file = request.FILES['profile_pic']
                #upload_image = User_image.objects.create(user=request.user, profile_pic=image_file,)
	else:
            #form = UserImageForm()
            return HttpResponseRedirect("/")
	return render(request, "user_image.html", {
        'form': form,
    })
	"""return render_to_response('user_image.html',
                {'user': request.user, 'form': form},
                context_instance=RequestContext(request))"""

@login_required
@is_profile
def settings(request):
	#user_id = request.user.id
	#inst = User_info.objects.get(user_id_id=user_id)
	form = SettingsForm()
	#instance = get_object_or_404(User_info, id=id)
	if request.method == 'POST':
		form = SettingsForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			#return HttpResponseRedirect("/accounts/add_interest/")
			#userinfo_o = User_info(username=request.user,)
			#userinfo_o.save()
		#else:
		#	form = EditProfileForm()
	else:
		form = SettingsForm(instance=request.user)
	return render(request, "settings.html", {
        'form': form,
    })


@login_required
def switch_profile(request):
	
	""" Check if business exists from session variable generated from signal """
	if request.session.get('business_exists') == 1:
		
		if not request.session.get('business'):
			request.session['business'] = 1
		elif request.session.get('business') == 1:
			request.session['business'] = 0
		elif request.session.get('business') == 0:
			request.session['business'] = 1
			
		if request.session['business'] == 1:
				return redirect('/office/')
		elif request.session['business'] == 0:
			return redirect('/profile/')
	else:
		return redirect('/')

@login_required
@is_profile
def bar_notifications(request):
	if request.is_ajax():

		user_info_obj = User_info.objects.filter(user_id=request.user.id)
		
		""" wish notifications """
		wish_id_list = Wish.objects.filter(user=user_info_obj).values('id')
		rewish_notify_obj = Feed.objects.filter(wish__in=wish_id_list).filter(status='A', feed_type__in = ('RW','RO','RR')).exclude(user=user_info_obj).order_by("-added")[:10]
		
		""" talk notifications """
		id_list = Talk_comment.objects.filter(user=user_info_obj).values('user','talk').annotate(Max('id')).values('id__max')
		talk_notify_obj = Talk_comment.objects.filter(pk__in=id_list).exclude(notify_count=0)[:10]
		
		""" friend requests received """
		invitations = FriendshipInvitation.objects.filter(to_user=request.user).order_by("-sent")
		
		""" friendships accepted """
		accepted_obj = Friendship.objects.filter(from_user=request.user).order_by("-added")
		
		if request.method == 'POST':
			if 'wish_read_id' in request.POST:
				""" Make clicked rewish notification as RR(Rewish Read) """
				Feed.objects.filter(id=request.POST['wish_read_id']).update(feed_type='RR')
			if 'wishes' in request.POST:
				""" Make all rewish notification as RO(Rewish Observed) on click on Wishes tab """
				Feed.objects.filter(wish__in=wish_id_list).filter(feed_type='RW').update(feed_type='RO')
		return render_to_response('base_notify.html',{'rewish_notify_obj': rewish_notify_obj, 'talk_notify_obj': talk_notify_obj, 'invitations': invitations, 'accepted_obj': accepted_obj},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/")

@login_required
@is_profile
def all_notifications(request):

	user_info_obj = User_info.objects.filter(user_id=request.user.id)
	
	""" wish notifications """
	wish_id_list = Wish.objects.filter(user=user_info_obj).values('id')
	rewish_notify_obj = Feed.objects.filter(wish__in=wish_id_list).filter(status='A', feed_type__in = ('RW','RO','RR')).exclude(user=user_info_obj).order_by("-added")
	
	""" talk notifications """
	id_list = Talk_comment.objects.filter(user=user_info_obj).values('user','talk').annotate(Max('id')).values('id__max')
	talk_notify_obj = Talk_comment.objects.filter(pk__in=id_list).exclude(notify_count=0).order_by("-added")
	
	""" friend requests received """
	invitations = FriendshipInvitation.objects.filter(to_user=request.user).order_by("-sent")
	
	""" friendships accepted """
	accepted_obj = Friendship.objects.filter(from_user=request.user).order_by("-added")
	
	""" talks test """
	talk_list = Talk.objects.filter(user=user_info_obj).values('id')
	comment_list = Talk_comment.objects.filter(talk__in=talk_list).filter(user=user_info_obj).values('talk').distinct()
	#my_talk_obj = Talk.objects.filter(pk__in=talk_list).exclude(pk__in=comment_list)
	my_talk_obj = Talk.objects.filter(user=user_info_obj).exclude(talk_comment__user=user_info_obj).exclude(talk_comment__user=None).order_by('-talk_comment__added')
	
	if request.method == 'POST':
		if 'wish_read_id' in request.POST:
			""" Make clicked rewish notification as RR(Rewish Read) """
			Feed.objects.filter(id=request.POST['wish_read_id']).update(feed_type='RR')
		if 'wishes' in request.POST:
			""" Make all rewish notification as RO(Rewish Observed) on click on Wishes tab """
			Feed.objects.filter(wish__in=wish_id_list).filter(feed_type='RW').update(feed_type='RO')
		if 'talks' in request.POST:
			""" Make notify_count of my top comment in all my talks as 0 """
			Talk_comment.objects.filter(user=user_info_obj).values('user','talk').annotate(Max('id')).update(notify_count = 0)
	return render_to_response('notifications.html',{'rewish_notify_obj': rewish_notify_obj, 'talk_notify_obj': talk_notify_obj, 'invitations': invitations, 'accepted_obj': accepted_obj, 'my_talk_obj': my_talk_obj},context_instance=RequestContext(request))

def common_feed_post(request):
	print 'inside feed_code'
	
	current_user = get_object_or_404(User_info, user_id_id=request.user.id)
	
	#if request.method == 'POST':
	if 're-wish' in request.POST:
		if Wish.objects.filter(id=request.POST['wish_id']).exists():
			wish_obj = Wish.objects.get(id=request.POST['wish_id'])
			feed_obj = Feed.objects.create(user=current_user, wish=wish_obj, feed_type='RW')
			wish_obj.rewish_count += 1
			wish_obj.save()
		else:
			raise Http404
	if 'share' in request.POST:
		bb_obj = Billboard.objects.get(id=request.POST['billboard_id'])
		if Feed.objects.filter(user=current_user, billboard=bb_obj).exists():
			feed_bb = Feed.objects.get(user=current_user, billboard=bb_obj)
			added_feed = (feed_bb.added).replace(tzinfo=None)
			current_feed = datetime.now()
			diff_feed = current_feed - added_feed
			if diff_feed.days < 1:
				error_message = 'You have recently shared this billboard, come back after 24 hours'
			else:
				feed_bb.added = datetime.now()
				feed_bb.save()
		else:
			feed_obj = Feed.objects.create(user=current_user, billboard=bb_obj, feed_type='SB')
	if 'rate' in request.POST:
		rating_obj = Rating_tag.objects.get(id=request.POST['rating_tag_id'])
		if Rating_owned.objects.filter(user=current_user, rating_tag=rating_obj).exists():
			owned_obj = Rating_owned.objects.get(user=current_user, rating_tag=rating_obj)
			added_rating = (owned_obj.added).replace(tzinfo=None)
			current_rating = datetime.now()
			diff_rating = current_rating - added_rating
			if diff_rating.days < 1:
				error_message = 'You have recently rated this tag, come back after 24 hours'
			else:
				old = owned_obj.rating
				new = request.POST['rated']
				diff = long(old) - long(new)
				owned_obj.rating = new
				#owned_obj.owned_type = request.POST['owned_type']
				owned_obj.save()
				
				old_rating = rating_obj.rating
				new_rating = (old_rating) - (diff)
				rating_obj.rating = new_rating
				rating_obj.save()
				
				feed_obj = Feed.objects.get(user=current_user, rating=owned_obj, feed_type='R')
				feed_obj.added = datetime.now()
				feed_obj.save()
		else:
			rating_obj.rating += long(request.POST['rated'])
			rating_obj.count += 1
			rating_obj.save()
						
			owned_obj = Rating_owned.objects.create(rating_tag=rating_obj, user=current_user, rating=request.POST['rated'])
			feed_obj = Feed.objects.create(user=current_user, rating=owned_obj, feed_type='R')
	if 'disable' in request.POST:
		print request.POST['wish_id']
		del_wish = Wish.objects.get(id=request.POST['wish_id'])
		if current_user == del_wish.user:
			del_wish.status = 'D'
			del_wish.save()
			
			del_feed = Feed.objects.filter(wish=del_wish).update(status='D')

from cities.models import City, Country
import json as simplejson

def autocomplete_city(request):
	term = request.GET.get('term') #jquery-ui.autocomplete parameter
    
	if term:
		# hard coding for India
		#country = Country.objects.filter(name='India')
		
		#cities = City.objects.filter(name__istartswith=term).filter(country=country) #lookup for a city
		cities = City.objects.filter(name__istartswith=term).filter(country_id=1269750) #lookup for a city
		res = []
		for c in cities:
			 #make dict with the metadatas that jquery-ui.autocomple needs (the documentation is your friend)
			 """ code commented to get only name """
			 #dict = {'id':c.id, 'label':c.__unicode__(), 'value':c.__unicode__()}
			 dict = {'value':c.name_std, 'label':c.name_std + ', ' + c.region.name_std, 'city':c.name_std, 'id':c.id}
			 res.append(dict)
			 #res.append(c.name)
		return HttpResponse(simplejson.dumps(res))
	else:
		return HttpResponseRedirect("/")

from django_facebook.decorators import facebook_required
from django.views.decorators.csrf import csrf_protect

@facebook_required(scope='publish_actions')
@csrf_protect
def custom_wall_post(request, link, graph):
	link = 'sellbig.in' + link
	graph.set('me/feed', link=link)

def autocomplete_tag(request):
	term = request.GET.get('term') #jquery-ui.autocomplete parameter

	if term:
		tags = Tag.objects.filter(name__istartswith=term)
		res = []
		for tag in tags:
			res.append(tag.name)
		return HttpResponse(simplejson.dumps(res))
	else:
		return HttpResponseRedirect("/")


from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.inputs import AutoQuery#, Exact, Clean

@page_template('search/search_feed.html')
def my_search(request, template='search/search.html', extra_context=None):

	data = {}
	if extra_context is not None:
		data.update(extra_context)

	search_cat = request.GET.get('cat', '')
	sub_cat = request.GET.get('sub_cat', '')
	min_price = request.GET.get('min_price', '')
	max_price = request.GET.get('max_price', '')
	location = request.GET.get('location', '')
	q = request.GET.get('q', '')
	sqs = SearchQuerySet().exclude(status='D')
	print "search_cat: " + search_cat
	print "sub_cat: " + sub_cat
	print "min_price: " + min_price
	print "max_price: " + max_price
	print "location: " + location
	print "q: " + q
	if q:
		print "if q"
		sqs = sqs.filter(content=AutoQuery(request.GET['q']))
	if search_cat:
		print "if search_cat"
		sqs = sqs.filter(category=search_cat)
	if sub_cat:
		print "if sub_cat"
		sqs = sqs.filter(subcategory=sub_cat)
	if min_price:
		print "if min_price"
		sqs = sqs.filter(price__gte=min_price)
	if max_price:
		print "if max_price"
		sqs = sqs.filter(price__lte=max_price)
	if location:
		print "if location"
		sqs = sqs.filter(location=location)
	sqs = sqs.order_by('-added')
	
	data['results'] = sqs
	return render_to_response(template, data, context_instance=RequestContext(request))
	#return render(request, "search/search.html", {'results': sqs})
