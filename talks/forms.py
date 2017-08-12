from django import forms
from talks.models import Talk, Talk_comment
from taggit.forms import *

class AddTalkForm(forms.ModelForm):
	description = forms.CharField(label='Description', required=True, max_length=500, widget=forms.Textarea)
	m_tags = TagField()
	class Meta:
		model = Talk
		fields = ("title", "description")

class AddCommentForm(forms.ModelForm):
	comment = forms.CharField(label='', required=False, widget=forms.Textarea)
	class Meta:
		model = Talk_comment
		fields = ("comment",)

class AddCommentReplyForm(forms.ModelForm):
	comment = forms.CharField(label='', required=False, widget=forms.Textarea)
	class Meta:
		model = Talk_comment
		fields = ("comment",)
