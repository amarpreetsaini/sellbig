#from django.db import models
from django import forms
from django.core.files.images import get_image_dimensions

from feed.models import Billboard
from taggit.forms import *

class AddWishForm(forms.Form):
	wish_text = forms.CharField(label='Wish-Box', widget=forms.Textarea)
	desc = forms.CharField(label='Wish-Box', widget=forms.Textarea)
	price = forms.IntegerField(label='Price', required=False)
	whatsapp_chk = forms.BooleanField(required=False)
	contact = forms.IntegerField(required=False)
	m_tags = TagField()

class BillboardForm(forms.ModelForm):
	class Meta:
		model = Billboard
		fields = ("billboard",)
	def clean_billboard(self):
		image = self.cleaned_data.get('billboard')
		if image:
			ext = image.content_type.split('/')[1]
			w, h = get_image_dimensions(image)
			if not ext in ('jpeg','jpg','png'):
				raise forms.ValidationError(u'Only *.jpeg, *.jpg and *.png images are allowed.')
			if (2 * w) < h:
				raise forms.ValidationError(u'Image size not proper.')
			if len(image) > (3 * 1024 * 1024):
				raise forms.ValidationError('Image file too large ( maximum 500kb )')
		return image

class AddOwnedForm(forms.Form):
	rating_choices = (
    ('5','5'),
    ('4','4'),
    ('3','3'),
    ('2','2'),
    ('1','1'),)
    
	owned_choices = (
    ('GT',u'Gadget'),
    ('VL',u'Vehicle'),
    ('BK',u'Book'),
    ('LB',u'Luxury brand'),
    ('O',u'Other'),)
	
	stuff_name = forms.CharField(label='I own')
	rating = forms.ChoiceField(choices=rating_choices, label="Rating")
	# commented as now we are not saving owned type, only 'MS' for my stuff and 'O' for others
	#owned_type = forms.ChoiceField(choices=owned_choices, label="Rating")
