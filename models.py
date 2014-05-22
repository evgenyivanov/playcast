from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink




class Playcast(models.Model):

    title = models.CharField(max_length=200)
    body =  models.TextField()
    width = models.CharField(max_length=6)
    height = models.CharField(max_length=6)
    style = models.CharField(max_length=400)
    mtitle = models.CharField(max_length=200)
    murl = models.CharField(max_length=200)
    mauthor = models.CharField(max_length=200)
    mperformer = models.CharField(max_length=200)
    comment =  models.TextField(blank=True)
    user = models.ForeignKey(User, editable = False)
    datetime = models.DateTimeField()
    last = models.DateTimeField()
    active = models.BooleanField()
    color1 = models.CharField(max_length=20)
    color2 = models.CharField(max_length=20)
    color3 = models.CharField(max_length=20)


class Readers(models.Model):

    user = models.ForeignKey(User, blank = True, null = True)
    ip = models.CharField(max_length=100)
    playcast = models.ForeignKey(Playcast, editable = False)
    date = models.DateTimeField()

class UserProfile(models.Model):

    user = models.ForeignKey(User, editable = False)
    photo = models.ImageField(upload_to='pic', blank=True)
    url = models.URLField( blank=True)
    about = models.TextField()


class Picture(models.Model):

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pic')
    key_words = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, editable = False, blank=True)
    datetime = models.DateTimeField()



    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('picture_detail', None, {'object_id': self.id})

class Music(models.Model):

    title = models.CharField(max_length=100)
    file = models.ImageField(upload_to='music')
    author = models.CharField(max_length=200)
    performer = models.CharField(max_length=200)
    key_words = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, editable = False, blank=True)
    datetime = models.DateTimeField()

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('picture_detail', None, {'object_id': self.id})