from django.contrib import admin
from account.models import Category, Subcategory

class CategoryAdmin(admin.ModelAdmin):
	#ordering = ['name_std']
	list_display = ['name', 'status', 'count', 'added']
	#search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

class SubcategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'category', 'status', 'count', 'added']

admin.site.register(Subcategory, SubcategoryAdmin)
