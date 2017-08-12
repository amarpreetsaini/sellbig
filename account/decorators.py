from django.shortcuts import redirect

def is_profile(fn):
	def deco(request, **kwargs):
		if not request.session.get('business'):
			return fn(request, **kwargs)
		elif request.session.get('business') == 1:
			return redirect("/office/")
		elif request.session.get('business') == 0:
			return fn(request, **kwargs)
	return deco

def is_business(fn):
	def deco(request, **kwargs):
		if not request.session.get('business'):
			return redirect("/profile/")
		elif request.session.get('business') == 1:
			return fn(request, **kwargs)
		elif request.session.get('business') == 0:
			return redirect("/profile/")
	return deco

def anonymous_required(f):
	def inner(request, *args, **kwargs):
		if not request.user.is_authenticated():
			return f(request, *args, **kwargs)
		else:
			return redirect("/")
	return inner
