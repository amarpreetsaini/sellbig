from django.db import models
from django.db.models import Q

class Business_usersManager(models.Manager):

	def business_for_user(self, user):
		businesses = []
		qs = self.filter(user=user)
		for connection in qs:
			businesses.append(connection.business)
		return businesses
