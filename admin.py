# coding: utf-8

from django.contrib import admin
#from django.db import models
from models import *


class PictureList(admin.ModelAdmin):
    fields = ('title', 'key_words','image')



admin.site.register(Picture, PictureList)
admin.site.register(Music)
admin.site.register(Playcast)
admin.site.register(UserProfile)
admin.site.register(Readers)
admin.site.register(LoginError)