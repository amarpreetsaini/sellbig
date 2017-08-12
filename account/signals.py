from django.contrib.auth.signals import user_logged_in

def test(sender, user, request, **kwargs):
	print 'in test'
	request.session['test'] = 'Tested OK'

print 'outsde test'
user_logged_in.connect(test)
