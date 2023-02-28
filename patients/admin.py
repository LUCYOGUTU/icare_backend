from django.contrib import admin
from .models import CustomUser, Review

admin.site.register(CustomUser)
admin.site.register(Review)
