# coding: utf-8

from django.contrib import admin
#from django.db import models
from models import Picture, Playcast,UserProfile


class PictureList(admin.ModelAdmin):
    fields = ('title', 'key_words','image')



admin.site.register(Picture, PictureList)
admin.site.register(Playcast)
admin.site.register(UserProfile)