# coding: utf-8

from django.contrib import admin
#from django.db import models
from models import *


class PictureList(admin.ModelAdmin):
    readonly_fields = ['picture_thumbnail','username',]
    fields = ('title', 'key_words','image')
    list_display = ('title','picture_thumbnail','key_words','username')

admin.site.register(Picture, PictureList)
admin.site.register(Music)

class PlaycastList(admin.ModelAdmin):
    readonly_fields = ['playcast_thumbnail','username',]
    list_display = ('title','username',"datetime")
admin.site.register(Playcast,PlaycastList)

admin.site.register(UserProfile)

class ReaderstList(admin.ModelAdmin):
    readonly_fields = ['author','username','title',]
    list_display = ('title','author','username',"date","ip")

admin.site.register(Readers,ReaderstList)

class LoginErrorList(admin.ModelAdmin):
    fields = ('ip', 'date')
    list_display = ('ip','date')

admin.site.register(LoginError,LoginErrorList)

class GiftsList(admin.ModelAdmin):
    readonly_fields = ['gift_thumbnail',]
    model = Gifts
    fields = ('title', 'gifts','price','days','gift_thumbnail')
    list_display = ('title','price','days','gift_thumbnail')
admin.site.register(Gifts,GiftsList)


class SendGiftsList(admin.ModelAdmin):
    readonly_fields = ['gift_thumbnail',]
    model = SendGifts

    list_display = ('fuser','tuser','price','date','gift_thumbnail')
admin.site.register(SendGifts,SendGiftsList)



class AccountList(admin.ModelAdmin):
    readonly_fields = ['username',]
    model = Account
    fields = ('date', 'sum','text','username')
    list_display = ('date', 'sum','text','username')

admin.site.register(Account,AccountList)