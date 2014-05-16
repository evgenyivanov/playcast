from django.http import HttpResponse
#from django import template
from django.template import Context
from django.template.loader import get_template
from forms import *
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.forms.util import ErrorList
#from django.shortcuts import render_to_response
import datetime
from models import Picture, Music,Playcast, UserProfile,Readers
import os, re
from PIL import Image
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


############################################################################
def readers(request,id):
    playcast = Playcast.objects.get(id = id)
    if playcast.user == request.user:
        list = Readers.objects.filter(playcast = playcast)

        L = []
        for i in list:
            L.append(i)
        d = {'L':L,'id':id,'title': playcast.title}
        t = get_template("readers.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)
    return HttpResponse('You is not author')


def author(request,id):
    usr = User.objects.get(id = id)
    profile = UserProfile.objects.filter(user = usr)[0]
    L=[]
    list = Playcast.objects.filter(user = usr).order_by('-datetime')

    for i in list:
       L.append(i)
    d = {'user':usr,'p':profile,'L':L}
    t = get_template("author.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)


@login_required
def editeprofile(request):

    if request.method == 'POST': # If the form has been submitted...

        formUser = UserForm(request.POST,request.FILES)
        formProfile = UserProFileForm(request.POST,request.FILES)

        if formUser.is_valid(): # and formProfile.is_valid() :
            request.user.first_name = formUser.cleaned_data['first_name']
            request.user.last_name = formUser.cleaned_data['last_name']
            request.user.email = formUser.cleaned_data['email']
            request.user.save()


            profile = UserProfile.objects.filter(user = request.user)[0]
            profile.url = request.POST['url']
            profile.about = request.POST['about']
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            profile.save()
            resault = 'You profile  update'

            return HttpResponse(resault)
        else:

             d = {'formProfile': formProfile,'formProfile':formProfile}
             d.update(csrf(request))
             t = get_template("userprofile.html")
             c = Context(d)
             html = t.render(c)
             return HttpResponse(html)

    else:

        profile = UserProfile.objects.filter(user = request.user)
        if profile.count() == 0:
            obj = UserProfile()
            obj.user = request.user
            obj.save()
        else:
            obj = profile[0]
        formUser = UserForm({'first_name':request.user.first_name,'last_name':request.user.last_name,'email':request.user.email})
        formProfile = UserProFileForm({'photo': obj.photo,'url':obj.url,'about':obj.about})
        d = {'formUser': formUser,'formProfile':formProfile}
        d.update(csrf(request))
        t = get_template("userprofile.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)




def mylogin(request):
    login2 = request.GET['login']
    passw = request.GET['password']
    user = authenticate(username=login2, password=passw)
    if user is not None:
        if user.is_active:
            login(request, user)
            html = 'Hello, <a href="/author/'+str(user.id)+'/">'+user.first_name+' '+user.last_name+'</a>!<br />'
            html = html +'<button type="button" onclick="document.location.href='
            html = html + "'/admin/logout/?next=/';"
            html = html +'">Log out</button>'
            html = html + '<br /><button onclick="EditeProfile();" >Edite profile</button>'
        else:
            pass
    else:
        html = 'Error: login and password<br />'
        html = html + '<br />login <input type="text" id ="login" value="">'
        html = html +'password <input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button>'




    return HttpResponse(html)

def home(request):

    user = request.user
    if str(user) == 'AnonymousUser':
        html = 'Hello, Guest!<br />login <input type="text" id ="login" value="">'
        html = html +'password <input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button>'
    else:
        html = 'Hello, <a href="/author/'+str(user.id)+'/">'
        html = html +  user.first_name+' ' + user.last_name
        html = html+ '</a>!<br />'
        html = html +'<button type="button" onclick="logout();">Log out</button>'
        html = html + '<br /><button onclick="EditeProfile();" >Edite profile</button>'
    d = {'mycode':html}
    t = get_template("index.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)



def playcast_list(request,arg = 0):
    list = Playcast.objects.all().order_by('-datetime')[int(arg): int(arg)+10]
    L1 = []
    for i in range(min(len(list),5)):
        L1.append(list[i])
    L2 = []
    n = len(list)-5
    for i in range(n):
        L2.append(list[i+5])
    links = ''

    if int(arg) > 9:
        links = '<a href = /playcast_list/'+str(int(arg)-10)+'/>Previos</a>  '
    if Playcast.objects.all().count > (int(arg)+10):
        links = links + '<a href = /playcast_list/'+str(int(arg)+10)+'/>Next </a>'
    d = {'L1':L1,'L2':L2,'links':links}
    t = get_template("playcast_list.html")
    c = Context(d)
    html = t.render(c)
    response = HttpResponse(html)
    response['Cache-Control'] = 'no-cache'
    return response

def deleteplaycast(request,id):

    obj = Playcast.objects.get(id=id)
    if obj.user == request.user:
        obj.delete()
        os.remove('/home/evgenyivanov/playcast/media/screen/'+str(id)+'.jpg')
        return redirect('/')


def playcast(request,id):

    obj = Playcast.objects.get(id=id)

    if obj.user != request.user:
        reader = Readers()
        try:
            reader.user = request.user
        except:
            pass
        reader.ip = str(request.META['REMOTE_ADDR'])
        reader.playcast = obj
        reader.date = datetime.datetime.now()
        reader.save()
    author=''
    if obj.user == request.user:
        author = '<a href = /designer/'+str(id)+'/>edite</a> <button onclick="DelQuest()">Delete</button><button onclick="Readers('+str(id)+');">Readers</button>'

    d = {'p':obj,'author':author,'tid':id}
    t = get_template("playcast.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)






@csrf_exempt
def put(request):

    if request.method == "POST":
        tid = request.POST['tid']
        if tid == '':
            obj = Playcast()
            obj.datetime = datetime.datetime.now()
        else:
            obj = Playcast.objects.get(id=tid)
        obj.title = request.POST['title']
        st = request.POST['body']
        st = st.replace('<div id="mybox" style="visibility:hidden"></div>','')
        st = st.replace('<script type="text/javascript" src="/static/js/jquery.js"></script>','')
        st = st.replace('<script type="text/javascript" src="/static/js/jquery.js"></script>','')
        st = st.replace('<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>','')
        st = st.replace('<script type="text/javascript" src="/static/js/ui/jquery.ui.core.js"></script>','')
        st = st.replace('<script type="text/javascript" src="/static/js/ui/jquery.ui.widget.js"></script>','')
        st = st.replace('<script type="text/javascript" src="/static/js/ui/jquery.ui.mouse.js</script>">','')
        st = st.replace('<script type="text/javascript" src="/static/js/ui/jquery.ui.draggable.js"></script>','')
        st = st.replace('<script type="text/javascript" src="/static/js/ui/jquery.ui.resizable.js"></script>','')
        st = st.replace('<script type="text/javascript" src="/static/js/jquery.ui.rotatable.js"></script>','')
        st = st.replace('<script type="text/javascript" src="/static/js/edite.js"></script>','')
        re.sub(r'\s+', ' ', st)
        obj.body = st
        obj.murl = request.POST['murl']
        obj.mtitle = request.POST['mtitle']
        obj.style = request.POST['style']
        obj.width = request.POST['width']
        obj.height = request.POST['height']
        obj.mauthor = request.POST['mauthor']
        obj.mperformer = request.POST['mperformer']
        obj.user = request.user
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
            obj.key_words = form.cleaned_data['key_words'].lower()
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

class Img():
    url = ''
    width = ''

def images_list(request):
    L=[]
    if str(request.GET['my']) == 'true':
        list = Picture.objects.filter(user = request.user).order_by('-datetime')
    else:
        list = Picture.objects.all().order_by('-datetime')

    keywords = request.GET['words'].lower()


    if len(keywords) > 0:
        keys = keywords.split()
        S= set()
        for i in keys:
            images = list.filter(key_words__contains = i)
            for j in images:
                S.add(j)

        L=[]
        for i in S:
            obj = Img()
            obj.url = '/media/'+ str(i.image)
            obj.width = str(102* i.image.width/i.image.height)
            L.append(obj)
        d = {'L':L[0:200]}
        t = get_template("imageslist.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)




    for i in list:
        obj = Img()
        obj.url = '/media/'+ str(i.image)
        obj.width = str(102* i.image.width/i.image.height)
        L.append(obj)
    d = {'L':L[0:200]}
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
            obj.key_words = form.cleaned_data['key_words'].lower()
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

@login_required
def designer(request, id = None):
    tid = ''
    tbody = ''
    title=''
    tstyle = 'background-color:#e0ffff;'
    twidth = '950px'
    theight = '750px'
    tmtitle =''
    tmurl = ''
    tmauthor = ''
    tmperformer = ''
    tcomment = ''

    if id != None:
        obj = Playcast.objects.get(id=id)

        if obj != None:
            if obj.user == request.user:
                title = obj.title
                tbody = obj.body
                tstyle = obj.style
                tid = obj.id
                twidth = obj.width
                theight = obj.height
                tmtitle = obj.mtitle
                tmurl = obj.murl
                tmauthor = obj.mauthor
                tmperformer = obj.mperformer
                tcomment = obj.comment


    d= {'tid':tid,'title':title,'tbody':tbody,'tstyle':tstyle,'twidth':twidth,'theight':theight,'tmtitle':tmtitle,'tmurl':tmurl,'tmauthor':tmauthor,'tmperformer':tmperformer,'tcomment':tcomment}
    t = get_template("designer.html")
    c = Context(d)
    html = t.render(c)
    response = HttpResponse(html)
    response['Cache-Control'] = 'no-cache'
    return response

def designer_body(request):
    d= {}
    t = get_template("designer_body.html")
    c = Context(d)
    html = t.render(c)
    response = HttpResponse(html)
    response['Cache-Control'] = 'no-cache'
    return response

def designer_menu(request):
    d= {}
    t = get_template("designer_menu.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)