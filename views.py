from django.http import HttpResponse
from django import template
from django.template import Context
from django.template.loader import get_template
from forms import *
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.forms.util import ErrorList
from django.shortcuts import render_to_response
import datetime
from models import Picture, Music
import os, re
from PIL import Image

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


############################################################################
@csrf_exempt
def put(request):

    if request.method == "POST":
        obj = Playcast()
        obj.title = request.POST['title']
        obj.body = request.POST['body']
        obj.murl = request.POST['murl']
        obj.mauthor = request.POST['mauthor']
        obj.mperformer = request.POST['mperformer']
        obj.user = request.user
        obj.datetime = datetime.datetime.now()
        obj.last = datetime.datetime.now()
        obj.save()
        return HttpResponse(obj.id)




@csrf_exempt
def save(request):

    if request.method == "POST":


        #path = os.path.join(os.path.dirname(__file__), 'static').replace('\\','/')
        #path = os.path.join(path, 'img').replace('\\','/')
        path = '/home/evgenyivanov/playcast/media/screen/'
        name = str(request.POST['id']) + '.jpg'
        path = os.path.join(path, name).replace('\\','/')
        fl = request.POST['imageData']
        imgstr = re.search(r'base64,(.*)', fl).group(1)
        output = open(path, 'wb')
        output.write(imgstr.decode('base64'))
        output.close()
        img = Image.open(path)
        size = 420, 420
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(path, "JPEG")

        return HttpResponse(path)

def select_music(request):
    d = {}
    t = get_template("selectmusic.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def music_list(request):
    L=[]
    list = Music.objects.all()
    for i in list:
        L.append(i)
    d = {'L':L}
    t = get_template("musiclist.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)


def upload_music(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UploadMusicForm(request.POST,request.FILES) # A form bound to the POST data
        if form.is_valid():
            obj = Music()
            obj.title = form.cleaned_data['title']
            obj.file = form.cleaned_data['file']
            obj.author = form.cleaned_data['author']
            obj.performer = form.cleaned_data['performer']
            obj.key_words = form.cleaned_data['key_words'].islower()
            obj.user = request.user
            obj.datetime = datetime.datetime.now()
            obj.save()

            return HttpResponse('Music uploated. Thank you!')
        else:
            d = form.errors
            form = UploadMusicForm()
            d = {'form': form}
            d.update(csrf(request))
            t = get_template("upload_music.html")
            c = Context(d)
            html = t.render(c)
            return HttpResponse(html)

    else:
        form = UploadMusicForm()
        d = {'form': form}
        d.update(csrf(request))
        t = get_template("upload_music.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)


def select_image(request):
    d = {}
    t = get_template("selectimage.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def images_list(request):
    L=[]
    list = Picture.objects.all()
    for i in list:
        L.append('/media/'+str(i.image))
    d = {'L':L}
    t = get_template("imageslist.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def upload_image(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UploadImageForm(request.POST,request.FILES) # A form bound to the POST data
        if form.is_valid():
            obj = Picture()
            obj.title = form.cleaned_data['name']
            obj.image = form.cleaned_data['file']
            obj.key_words = form.cleaned_data['key_words'].islower()
            obj.user = request.user
            obj.datetime = datetime.datetime.now()
            obj.save()

            return HttpResponse('Image uploated. Thank you!')
        else:
            d = form.errors

            form = UploadImageForm()
            d = {'form': form}
            d.update(csrf(request))
            t = get_template("upload.html")
            c = Context(d)
            html = t.render(c)
            return HttpResponse(html)

    else:
        form = UploadImageForm()
        d = {'form': form}
        d.update(csrf(request))
        t = get_template("upload.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)


def designer(request):
    d= {}
    t = get_template("designer.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def designer_body(request):
    d= {}
    t = get_template("designer_body.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def designer_menu(request):
    d= {}
    t = get_template("designer_menu.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)