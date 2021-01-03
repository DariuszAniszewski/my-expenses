from django.contrib import admin

# Register your models here.
from core.models import Category, SubCategory, Place

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Place)
