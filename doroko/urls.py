from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

import account.views
import feed.views
import talks.views
import messages.views
import account.decorators


from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
#sqs = SearchQuerySet().facet('wish_text').facet('title')
#sqs = SearchQuerySet().autocomplete()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    
    # for autocomplete
    url(r'^autocomplete_city/$', account.views.autocomplete_city, name='autocomplete_city',),
    
    # for autocomplete
    url(r'^autocomplete_tag/$', account.views.autocomplete_tag, name='autocomplete_tag',),

    # for Find friends
    url(r'^find_friends/$', account.views.find_friends, name='find_friends',),

    # for Invite friends
    url(r'^invite_friends/$', account.views.invite_friends, name='invite_friends',),
    
    # for django_facebook
    (r'^facebook/', include('django_facebook.urls')),
    
    url(r'^notifications/$', account.views.all_notifications, name='notifications',),
    url(r'^bar_notifications/$', account.views.bar_notifications, name='bar_notifications',),
    
    url(r'^wishbox/$', feed.views.add_wish, name='wishbox'),
    url(r'^wish/(?P<wish_slug>[-\w]+)/$', feed.views.get_wish, name='wish'),
    url(r'^edit-post/(?P<wish_slug>[-\w]+)/$', feed.views.edit_wish, name='edit_wish'),
    
    url(r'^owned_stuff/$', feed.views.add_owned_stuff, name='add_owned_stuff'),

    url(r'^profile/$', account.views.profile, name='profile'),
    url(r'^office/$', account.views.my_office, name='my_office'),
    url(r'^switch/$', account.views.switch_profile, name='switch_profile'),
    url(r'^edit_business/$', account.views.add_business, name='add_business'),
    url(r'^image/$', account.views.user_image, name='user_image'),
    url(r'^billboard/$', feed.views.add_billboard, name='add_billboard'),
    url(r'^business_logo/$', account.views.add_logo, name='add_logo'),
    
    url(r'^talks/$', talks.views.add_talk, name='talks'),
    
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^search/', include('haystack.urls')),
    url(r'^search/$', account.views.my_search, name='my_search'),
    
    url(r'^accounts/login/$',  account.decorators.anonymous_required(login), {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/accounts/login/'}, name='logout',),
    #url(r'^accounts/home/$', feed.views.home_feed, name='home'),
    url(r'^accounts/signup/$', account.views.register, name='signup'),
    url(r'^accounts/edit_profile/$', account.views.edit_profile, name='edit_profile'),
    url(r'^accounts/add_interest/$', account.views.newuser, name='add_interest',),
    url(r'^accounts/settings/$', account.views.settings, name='settings',),
    url(r'^accounts/password-change/$', password_change, {'template_name': 'password_change.html', 'post_change_redirect': 'settings'}, name='password_change'),
    #url(r'^change-password-done/$', password_change_done, {'template_name': 'password_change_done.html'}, name="password_change_done"),
    
    # Following for forget password
    url(r'^user/password/reset/$', password_reset, {'template_name': 'password_reset_form.html', 'email_template_name': 'password_reset_email.html',  'post_reset_redirect' : '/user/password/reset/done/'}, name="password_reset"),
    url(r'^user/password/reset/done/$', password_reset_done, {'template_name': 'password_reset_done.html'}, name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'password_reset_confirm.html', 'post_reset_redirect' : '/user/password/done/'}),
    url(r'^user/password/done/$', password_reset_complete, {'template_name': 'password_reset_complete.html'}),
    
    url(r'^messages/$', messages.views.send_message, name='messages',),
    url(r'^messages/(?P<username>[\.\w]+)$', messages.views.message_chat, name='message_chat',),
    
    url(r'^friends/', include('friends.urls'),),
    url(r'^talks/(?P<slug>[-\w]+)/$', talks.views.talk_comment, name='talk_comment',),
    
    url(r'^policy/$', TemplateView.as_view(template_name="privacy_policy.html"), name='policy'),
    url(r'^terms/$', TemplateView.as_view(template_name="terms_of_use.html"), name='terms'),
    url(r'^about/$', TemplateView.as_view(template_name="about_us.html"), name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name="contact_us.html"), name='contact'),
    
    url(r'^(?P<username>[\.\w]+)/$', account.views.profile_detail, name='profile_detail',),
    url(r'^business/(?P<off_tag>[\.\w]+)/$', account.views.business_detail, name='business_detail',),
    url(r'^(?P<username>[\.\w]+)/contacts/$', account.views.profile_contacts, name='profile_contacts',),
    url(r'^business/(?P<off_tag>[\.\w]+)/contacts/$', account.views.business_contacts, name='business_contacts',),
    
    # Cover page url
    #url(r'^$', account.decorators.anonymous_required(TemplateView.as_view(template_name='cover.html'))),
    url(r'^$', feed.views.home_feed, name='home'),
    
)
#urlpatterns += patterns('haystack.views',
#    url(r'^$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
#)
urlpatterns += staticfiles_urlpatterns()
