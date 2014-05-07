from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink

class Playcast(models.Model):

    title = models.CharField(max_length=200)
    body =  models.TextField()
    width = models.CharField(max_length=4)
    height = models.CharField(max_length=4)
    style = models.CharField(max_length=400)
    mtitle = models.CharField(max_length=200)
    murl = models.CharField(max_length=200)
    mauthor = models.CharField(max_length=200)
    mperformer = models.CharField(max_length=200)
    comment =  models.TextField()
    user = models.ForeignKey(User, editable = False)
    datetime = models.DateTimeField()
    last = models.DateTimeField()


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