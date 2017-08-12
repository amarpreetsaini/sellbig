from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.template import RequestContext

from feed.forms import AddWishForm, BillboardForm, AddOwnedForm
from feed.models import Wish, Billboard, Feed, Activity, Rating_tag, Rating_owned, Wish_image, Category, Subcategory
from account.models import User_info, Business, Business_users
from account.decorators import is_profile, is_business
from account.views import custom_wall_post, common_feed_post
from talks.models import Talk, Talk_comment
from talks.forms import AddTalkForm
from friends.models import Friendship
from taggit.models import Tag
from cities.models import City
from endless_pagination.decorators import page_templates, page_template

from itertools import chain
from operator import attrgetter
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import utc
import uuid


import json as simplejson
import json
from django.http import HttpResponse


"""import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
   """ 

"""@login_required
@is_profile
def add_wish(request):
	
	#View to add a new wish by a user
	
	form = AddWishForm()
	if request.method == 'POST':
		form = AddWishForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			m_tags = form.cleaned_data['m_tags']
			user_info_obj = User_info.objects.get(user_id=request.user)
			wish = Wish.objects.create(user=user_info_obj, wish_text=cd['message'])
			feed_obj = Feed.objects.create(user=user_info_obj, wish=wish, feed_type='W')
			wish.tags.add(*m_tags)
			return HttpResponseRedirect("/wishbox/")
	else:
		form = AddWishForm()
	return render(request, "wishbox.html", {
			'form': form,
		})"""

@login_required
@is_profile
def add_wish_bk(request):
	"""
	View to add a new wish by a user
	"""
	
	#results = {'success':False}
	#form = AddWishForm()
	#if request.method == u'GET':
	#	GET = request.GET
	#	if GET.has_key(u'pk') and GET.has_key(u'vote'):
	#		pk = int(GET[u'pk'])
	#		vote = GET[u'vote']
	#		
	#		results = {'success':True}
	#json = simplejson.dumps(results)
	#return HttpResponse(json, mimetype='application/json')
	
	
	if request.method == 'POST' and request.is_ajax:
		form = AddWishForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			m_tags = form.cleaned_data['m_tags']
			user_info_obj = User_info.objects.get(user_id=request.user)
			wish = Wish.objects.create(user=user_info_obj, wish_text=cd['message'])
			feed_obj = Feed.objects.create(user=user_info_obj, wish=wish, feed_type='W')
			wish.tags.add(*m_tags)
			message = request.POST['message']
			#return HttpResponseRedirect("/wishbox/")
			returnedJSON = {}
			returnedJSON['message_type'] = 'success'
			returnedJSON['message'] = 'The something saved successfully'
			form = AddWishForm()
		return HttpResponse(simplejson.dumps(form), mimetype="application/json")
		#return HttpResponse(json.dumps({'message': message}))
	else:
		form = AddWishForm()
	return render(request, "wishbox.html", {
			'form': form,
		})

@login_required
@is_profile
def add_wish(request):
	"""
	View to add a new wish by a user
	"""
	
	wish_form = AddWishForm()
	cat_obj = Category.objects.filter(status='A')
	if request.method == 'POST':
		wish_form = AddWishForm(request.POST)
		if wish_form.is_valid():
			cd = wish_form.cleaned_data
			m_tags = wish_form.cleaned_data['m_tags']
			if request.POST['search-city2-id'] and request.POST['wish-cat'] and request.POST['sub-cat'] and request.POST['filter-radio']:
				user_info_obj = User_info.objects.get(user_id=request.user)
				city_obj = City.objects.get(id=request.POST['search-city2-id'])
				cat_obj = Category.objects.get(id=request.POST['wish-cat'])
				sub_obj = Subcategory.objects.get(id=request.POST['sub-cat'])
				
				wish = Wish.objects.create(
										user=user_info_obj,
										wish_text=(cd['wish_text'])[0:150],
										desc=(cd['desc'])[0:500],
										price=(cd['price']),
										category=cat_obj,
										subcategory=sub_obj,
										wish_type=request.POST['filter-radio'],
										location=city_obj,
										whatsapp_chk=cd['whatsapp_chk'],
										contact=cd['contact']
										)
				slug = slugify(cd['wish_text'])[0:70] + '-' + str(wish.id)
				wish.slug = slug
				wish.save()
				
				for tag in m_tags:
					wish.tags.add(tag.lower())
				if request.POST['filter-radio'] == 'sell':
					for img in request.FILES.getlist('wishimages[]'):
						ext = img.content_type.split('/')[1]
						name = uuid.uuid4()
						img.name = str(name) + '.' + str(ext)
						wish_image = Wish_image.objects.create(wish=wish, image=img)
				
				feed_obj = Feed.objects.create(user=user_info_obj, wish=wish, feed_type='W')
				
				""" Check whether checkbox to post to Facebook is checked or not """
				if 'fb-chk' in request.POST:
					print "ethe"
					print request.user.facebook_id
					if request.user.facebook_id:
						print "lol"
						link = "/wish/"+slug+"/"
						custom_wall_post(request, link)
				
				wish_form = AddWishForm()
				return HttpResponseRedirect("/wish/"+slug+"/")
				
	return render(request, 'wishbox.html', {'wish_form': wish_form, 'cat_obj': cat_obj})

@is_profile
def get_wish(request, wish_slug):
	"""
	View to get wish page
	"""
	
	wish_obj = get_object_or_404(Wish, slug=wish_slug)
	
	if request.method == 'POST':
		common_feed_post(request)
	"""if request.method == 'POST':
		if 'wish_id' in request.POST:
			del_wish = Wish.objects.get(id=request.POST['wish_id'])
			del_wish.status = 'D'
			del_feed = Feed.objects.filter(wish=del_wish)
			del_feed.status = 'D'
			del_feed.save()"""
	return render(request, 'wish.html', {'wish_obj': wish_obj})


@login_required
@is_profile
def edit_wish(request, wish_slug):
	"""
	View to edit wish page
	"""
	
	wish_obj = get_object_or_404(Wish, user=request.user.user_info, slug=wish_slug)
	
	if request.method == 'POST':
		print "edit post POST"
		if request.POST['wish_text']:
			wish_obj.wish_text = request.POST['wish_text'][0:150]
		if request.POST['desc']:
			print "edit post desc"
			wish_obj.desc = request.POST['desc'][0:500]
		if request.POST['price']:
			wish_obj.price = request.POST['price']
		wish_obj.added = datetime.now()
		wish_obj.save()
		feed_obj = Feed.objects.get(wish=wish_obj)
		feed_obj.added = wish_obj.added
		feed_obj.save()
		return HttpResponseRedirect("/wish/"+wish_obj.slug+"/")

	return render(request, 'edit_wish.html', {'wish_obj': wish_obj})

@login_required
@is_business
def add_billboard(request):
	"""
	View to add billboard to a business
	"""
	form = BillboardForm()
	if request.method == 'POST':
            form = BillboardForm(request.POST, request.FILES)
            if form.is_valid():
				if 'billboard' in request.FILES:
					ext = request.FILES['billboard'].content_type.split('/')[1]
					name = uuid.uuid4()
					request.FILES['billboard'].name = str(name) + '.' + str(ext)
					
					business = Business.objects.get(user=request.user)
					billboard = Billboard.objects.create(business=business, billboard=request.FILES['billboard'])
					feed_obj = Feed.objects.create(business=business, billboard=billboard, feed_type='B')
				else:
					form = BillboardForm()
				return HttpResponseRedirect("/office")
	else:
            #form = BillboardForm()
            return HttpResponseRedirect("/office")
	return render(request, "billboard.html", {
        'form': form,
    })
	"""return render_to_response('user_image.html',
                {'user': request.user, 'form': form},
                context_instance=RequestContext(request))"""

@login_required
@is_profile
def add_owned_stuff(request):
	"""
	View to rate (and add) owned stuff, business or random tag
	"""
	error_message = 'null'
	#form = AddOwnedForm()
	user_info_obj = User_info.objects.get(user_id=request.user)
	if request.method == 'POST':
		print 'add stuff>> POST'
		if 'add-stuff' in request.POST:
			form = AddOwnedForm(request.POST)
			if form.is_valid():
				print 'add stuff>> form valid'
				cd = form.cleaned_data
				#m_tags = form.cleaned_data['m_tags']
					
				# Checks for tag already there in Tag table
				if Tag.objects.filter(name=cd['stuff_name']).exists():
					tag_obj = Tag.objects.get(name=cd['stuff_name'])
					
					# Checks for tag already there in Rating_tag table, then update the existing value
					if Rating_tag.objects.filter(tag=tag_obj).exists():
						rating_obj = Rating_tag.objects.get(tag=tag_obj)
							
						if Rating_owned.objects.filter(rating_tag=rating_obj, user=user_info_obj).exists():
							owned_obj = Rating_owned.objects.get(rating_tag=rating_obj, user=user_info_obj)
							if owned_obj.owned_type == 'O':
								old = owned_obj.rating
								new = cd['rating']
								diff = long(old) - long(new)
								owned_obj.rating = new
								# commented as now we are not saving owned type, only 'MS' for my stuff and 'O' for others
								#owned_obj.owned_type = cd['owned_type']
								owned_obj.owned_type = 'MS'
								owned_obj.save()
								
								old_rating = rating_obj.rating
								new_rating = (old_rating) - (diff)
								rating_obj.rating = new_rating
								rating_obj.save()
								
								feed_obj = Feed.objects.create(user=user_info_obj, rating=owned_obj, feed_type='R')
							else:
								error_message = 'Product already there in your owned list'
								print error_message
						else:
							rating_obj.rating += long(cd['rating'])
							rating_obj.count += 1
							rating_obj.save()
								
							owned_obj = Rating_owned.objects.create(rating_tag=rating_obj, user=user_info_obj, rating=cd['rating'], owned_type='MS')#cd['owned_type'])
							feed_obj = Feed.objects.create(user=user_info_obj, rating=owned_obj, feed_type='R')
								
						
					# Checks for tag not in Rating_tag table, then create a new entry
					else:
						rating_obj = Rating_tag.objects.create(tag=tag_obj, rating=cd['rating'], count=1)
						owned_obj = Rating_owned.objects.create(rating_tag=rating_obj, user=user_info_obj, rating=cd['rating'], owned_type='MS')#cd['owned_type'])
						feed_obj = Feed.objects.create(user=user_info_obj, rating=owned_obj, feed_type='R')
					
				# Checks for tag not in Tag table, then create a new entry
				else:
					print 'add stuff>> tags else'
					slug = slugify(cd['stuff_name'])
					tag_obj = Tag.objects.create(name=(cd['stuff_name'].lower()), slug=slug)
					rating_obj = Rating_tag.objects.create(tag=tag_obj, rating=cd['rating'], count=1)
					owned_obj = Rating_owned.objects.create(rating_tag=rating_obj, user=user_info_obj, rating=cd['rating'], owned_type='MS')#cd['owned_type'])
					feed_obj = Feed.objects.create(user=user_info_obj, rating=owned_obj, feed_type='R')
				
				return HttpResponseRedirect("/owned_stuff/")
		elif 'delete-stuff' in request.POST:
			del_owned_obj = Rating_owned.objects.get(id=request.POST['stuff_id'])
			del_owned_obj.delete()
			return HttpResponseRedirect("/owned_stuff/")
	else:
		form = AddOwnedForm()
	print error_message
	all_owned_obj = Rating_owned.objects.filter(user=user_info_obj).exclude(owned_type='O')
	return render(request, "owned_stuff.html", {'form': form, 'error_message': error_message, 'all_owned_obj': all_owned_obj})

@page_templates((('feed.html', None), ('activity.html', 'activity'),))
#@login_required
@is_profile
def home_feed(request, template='landing.html', extra_context=None):
	"""
	View to display feed on feed page
	"""
	
	if not request.user.is_authenticated():
		return render(request, "cover.html")
	else:
		data = {}
		if extra_context is not None:
			data.update(extra_context)
			
		friends = Friendship.objects.friends_for_user(request.user)
		user_info = User_info.objects.filter(user_id__in=friends)
		
		try:
			user_info_obj = User_info.objects.get(user_id_id=request.user.id)
		except User_info.DoesNotExist:
			#current_user = User_info(user_id=request.user)
			#current_user.save()
			return HttpResponseRedirect("/accounts/edit_profile/")
		else:
			current_user = User_info.objects.get(user_id_id=request.user.id)
		
		#current_user = get_object_or_404(User_info, user_id_id=request.user.id)
		businesses = Business_users.objects.business_for_user(current_user)
		
		error_message = 'null'
		
		if request.method == 'POST':
			if 'location' in request.POST and request.POST.get('location'):
				user_info_obj.location_id = request.POST.get('location')
				user_info_obj.save()
			common_feed_post(request)

		talk_form = AddTalkForm()
		
		feed_obj = Feed.objects.filter(Q(user__in=user_info) | Q(business__in=businesses) | (Q(wish__location=user_info_obj.location) & Q(feed_type__in=('W', 'RW')))).filter(status='A').order_by("-added")
		#activity_obj = Activity.objects.filter(Q(user__in=user_info) | Q(business__in=businesses)).filter(status='A').order_by("-added")
		
		""" To send activity object to the template """
		friend_obj = Friendship.objects.filter(Q(from_user__in=friends) | Q(to_user__in=friends)).exclude(Q(from_user=request.user) | Q(to_user=request.user))
		business_obj = Business_users.objects.filter(user__in=user_info)
		comment_obj = Talk_comment.objects.filter(user__in=user_info)
		#activity_obj = list(chain(business_obj, comment_obj, friend_obj))
		activity_obj = sorted(
		chain(business_obj, comment_obj, friend_obj),
		key=attrgetter('added'),
		reverse=True)
		
		""" Sent to template to make rewish button enabled or disabled """
		rewish_obj = Feed.objects.values_list('wish', flat=True).filter(user_id=current_user, feed_type__in=('W', 'RW'))
		
		""" new talk object for trending talks """
		last_week = datetime.utcnow().replace(tzinfo=utc) - timedelta(days=7)
		trending_talks_obj = Talk.objects.filter(added__gte=last_week).order_by('-comments_count','-added')[:3]
		
		cat_obj = Category.objects.filter(status='A')
		
		data['feed_obj'] = feed_obj
		data['activity_obj'] = activity_obj
		data['rewish_obj'] = rewish_obj
		data['error_message'] = error_message
		data['talk_form'] = talk_form
		data['trending_talks_obj'] = trending_talks_obj
		data['cat_obj'] = cat_obj

		#return render(request, 'welcome.html', {'feed_obj': feed_obj, 'activity_obj': activity_obj, 'rewish_obj': rewish_obj, 'error_message': error_message, 'talk_form': talk_form})
		return render_to_response(template, data, context_instance=RequestContext(request))
