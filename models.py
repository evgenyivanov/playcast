from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink

class Account(models.Model):
    date = models.DateTimeField()
    sum = models.IntegerField()
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, editable = False)

    def username(self):
        return self.user.username


class Gifts(models.Model):
    title = models.CharField(max_length=200)
    gifts = models.ImageField(upload_to='gifts', blank=True)
    price = models.IntegerField()
    days = models.IntegerField()
    period = models.IntegerField()

    def gift_thumbnail(self):
        if self.gifts:
            return u'<img width="45" height="45" src="%s" />' % (self.gifts.url)
        else:
            return '(Sin imagen)'
    gift_thumbnail.short_description = 'Thumbnail'
    gift_thumbnail.allow_tags = True

class SendGifts(models.Model):
    fuser = models.IntegerField()
    tuser = models.IntegerField()
    gift = models.ForeignKey(Gifts, editable = False)
    price = models.IntegerField()
    date = models.DateTimeField()

    def gift_thumbnail(self):
        if self.gifts:
            return u'<img width="45" height="45" src="%s" />' % (self.gift.gifts.url)
        else:
            return '(Sin imagen)'
    gift_thumbnail.short_description = 'Thumbnail'
    gift_thumbnail.allow_tags = True


class LoginError(models.Model):
    ip =  models.CharField(max_length=100)
    date = models.DateTimeField()



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

    def username(self):
        return self.user.username

    def playcast_thumbnail(self):
        if self.image:
            return u'<img width="250" height="250" src="/media/screen/%s.jpg" />' % (self.id)
        else:
            return '(Sin imagen)'
    playcast_thumbnail.short_description = 'Thumbnail'
    playcast_thumbnail.allow_tags = True


class Readers(models.Model):

    user = models.ForeignKey(User, blank = True, null = True)
    ip = models.CharField(max_length=100)
    playcast = models.ForeignKey(Playcast, editable = False)
    date = models.DateTimeField()

    def username(self):
        return self.user.username

    def author(self):
        return self.playcast.user.username

    def title(self):
        return self.playcast.title


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

    def picture_thumbnail(self):
        if self.image:
            return u'<img width="45" height="45" src="%s" />' % (self.image.url)
        else:
            return '(Sin imagen)'
    picture_thumbnail.short_description = 'Thumbnail'
    picture_thumbnail.allow_tags = True

    def username(self):
        return self.user.username



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