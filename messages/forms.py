from django import forms
from messages.models import Message, Thread

class SendMessageForm(forms.Form):
	text = forms.CharField(max_length=500, label='Message', required=False, widget=forms.Textarea)
	#class Meta:
	#	model = Message
	#	fields = ("text",)
