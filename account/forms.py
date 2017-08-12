from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files.images import get_image_dimensions

from account.models import User_info, Business
from taggit.forms import *

from django_facebook.models import FacebookCustomUser

from django.conf import settings

class RegisterForm(UserCreationForm):
	
	class Meta:
		model = get_user_model()
		fields = ("username", "password1", "password2", "email", "first_name", "last_name",)
		
	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		
		if commit:
			user.save()
		return user
		
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if username in settings.RESERVED_URLS:
			raise forms.ValidationError(u'User with this Username not allowed.')
		return username
	
	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		#if email and User.objects.filter(email=email).exclude(username=username).count():
		if email and FacebookCustomUser.objects.filter(email=email).count():
			raise forms.ValidationError(u'A user with that email already exists.')
		return email

class EditProfileForm(forms.ModelForm):
	#about_tags = TagField()
	class Meta:
		model = User_info
		exclude = ('user_id', 'dob', 'gender', 'avatar','city','state','country','location')

class UserImageForm(forms.ModelForm):
	class Meta:
		model = User_info
		fields = ("avatar",)
		#exclude = ('user')
		
	def clean_avatar(self):
		image = self.cleaned_data.get('avatar')
		if image:
			ext = image.content_type.split('/')[1]
			w, h = get_image_dimensions(image)
			if not ext in ('jpeg','jpg','png'):
				raise forms.ValidationError(u'Only *.jpeg, *.jpg and *.png images are allowed.')
			if (2 * w) < h:
				raise forms.ValidationError(u'Image size not proper.')
			if len(image) > (3 * 1024 * 1024):
				raise forms.ValidationError('Image file too large ( maximum 3mb )')
		return image

class AddBusinessForm(forms.ModelForm):
	#tags = TagField()
	class Meta:
		model = Business
		exclude = ('user', 'member_count', 'visit_count', 'logo')

class SettingsForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ("email", "first_name", "last_name",)

class LogoForm(forms.ModelForm):
	class Meta:
		model = Business
		fields = ("logo",)
	def clean_logo(self):
		image = self.cleaned_data.get('logo')
		if image:
			ext = image.content_type.split('/')[1]
			w, h = get_image_dimensions(image)
			if not ext in ('jpeg','jpg','png'):
				raise forms.ValidationError(u'Only *.jpeg, *.jpg and *.png images are allowed.')
			if (2 * w) < h:
				raise forms.ValidationError(u'Image size not proper.')
			if len(image) > (0.5 * 1024 * 1024):
				raise forms.ValidationError('Image file too large ( maximum 500kb )')
		return image
