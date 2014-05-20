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
#from django.core.exceptions import ValidationError
from capcha import capthaGenerate
import hashlib

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


############################################################################
def register(request):
    captcha=  capthaGenerate(request)
    mm = hashlib.md5()
    mm.update(captcha[1])


    if request.method == 'POST': # If the form has been submitted...

        formUser = RegUserForm(request.POST)
        passw1 = request.POST['passw1']
        passw2 = request.POST['passw2']
        m = hashlib.md5()
        m.update(request.POST['captcha'])
        captha_input = m.hexdigest()
        captcha_value = request.POST['capcha_value']
        user_count = len(User.objects.filter(username = request.POST['username']))


        if formUser.is_valid() and (passw1 == passw2) and (captha_input == captcha_value) and (user_count == 0):

            new_user  = User.objects.create_user(username=formUser.cleaned_data['username'],
                                 email=formUser.cleaned_data['email'],
                                 password=passw1)
            new_user. is_active = True
            new_user.first_name=formUser.cleaned_data['first_name'],
            new_user.last_name=formUser.cleaned_data['last_name'],
            new_user.save()

            return redirect('/')
        else:

             d = {'formUser': formUser}
             if user_count > 0:
                 d.update({'username_error':"username is already used"})
             if passw1 != passw2:
                 d.update({'password_error':"Passwords don't match"})
             if (captha_input != captcha_value):
                 d.update({'captcha_error':"Captcha don't match"})

             d.update({'captcha':captcha[0],'capcha_value': mm.hexdigest()})
             d.update(csrf(request))
             t = get_template("register.html")
             c = Context(d)
             html = t.render(c)
             return HttpResponse(html)

    else:

        formUser = RegUserForm()
        d = {'captcha':captcha[0],'capcha_value': mm.hexdigest(),'formUser': formUser}
        d.update(csrf(request))
        t = get_template("register.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)







def readers(request,id):
    playcast = Playcast.objects.get(id = id)
    if playcast.user == request.user:
        list = Readers.objects.filter(playcast = playcast)
        total=len(list)

        L = []
        for i in list:
            L.append(i)
        d = {'L':L,'id':id,'title': playcast.title,'total': total}
        t = get_template("readers.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)
    return HttpResponse('You is not author')


def author(request,id):
    usr = User.objects.get(id = id)
    profile = UserProfile.objects.filter(user = usr)[0]
    if str(profile.photo) == '':
        url_img = '/static/images/no_image.gif'
        h = 250
    else:
        url_img = '/media/'+str(profile.photo)
        h = 250 * profile.photo.height / profile.photo.width
    L=[]
    if request.user == usr:
        list = Playcast.objects.filter(user = usr).order_by('-datetime')
    else:
        list = Playcast.objects.filter(user = usr).filter(active = True).order_by('-datetime')

    for i in list:
       L.append(i)
    d = {'user':usr,'p':profile,'L':L,'url_img':url_img,'h':h}
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
            resault = '<head><script src="//code.jquery.com/jquery-1.9.1.js'+'"></script>'
            resault = resault + '<script src="/static/js/admin.js'+'"></script></head><body>'
            resault = resault + '<body onload="EndEditeProfile('+"'"+"'"+');'+'">OK</body>'

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
            html = 'Hello, <a href="/author/'+str(user.id)+'/" target = "_blank'+'">'+user.first_name+' '+user.last_name+'</a>!<br />'
            html = html + '<button onclick="EditeProfile();" >Edite profile</button>'
            html = html +'<button type="button" onclick="document.location.href='
            html = html + "'/accounts/logout/?next=/';"
            html = html +'">Log out</button>'

        else:
            pass
    else:
        html = '<span style="color: red;'+'">Error: login and password</span>'
        html = html + '<br />login <span style="position:relative;left:4px;"><input type="text" id ="login" value=""></span>'
        html = html +'password <input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button> or <a href="/register">Sign up</a>'




    return HttpResponse(html)

def CurrentUser(request):

    user = request.user
    if str(user) == 'AnonymousUser':
        html = 'Hello, Guest!<br />login <span style="position:relative;left:4px;"><input type="text" id ="login" value=""></span>'
        html = html +'password <input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button> or <a href="/register">Sign up</a>'
    else:
        html = 'Hello, <a href="/author/'+str(user.id)+'/" target = "_blank'+'">'
        html = html +  user.first_name+' ' + user.last_name
        html = html+ '</a>!<br />'
        html = html + '<button onclick="EditeProfile();" >Edite profile</button>'
        html = html +'<button type="button" onclick="logout();">Log out</button>'
    return HttpResponse(html)

def home(request):

    user = request.user
    if str(user) == 'AnonymousUser':
        html = 'Hello, Guest!<br />login <span style="position:relative;left:29px;"><input type="text" id ="login" value=""></span>'
        html = html +'password <input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button> or <a href="/register">Sign up</a>'
    else:
        html = 'Hello, <a href="/author/'+str(user.id)+'/" target = "_blank'+'">'
        html = html +  user.first_name+' ' + user.last_name
        html = html+ '</a>!<br />'
        html = html + '<button onclick="EditeProfile();" >Edite profile</button>'
        html = html +'<button type="button" onclick="logout();">Log out</button>'
    d = {'mycode':html}
    t = get_template("index.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)



def playcast_list(request,arg = 0):
    list = Playcast.objects.filter(active = True).order_by('-datetime')[int(arg): int(arg)+10]
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
    if len(Playcast.objects.all()) > (int(arg)+10):
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
        os.remove('/home/playcards/playcast/media/screen/'+str(id)+'.jpg')
        return redirect('/')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def playcast(request,id):
    noactive = ''
    obj = Playcast.objects.get(id=id)
    if obj.active != True:
        if obj.user != request.user:
            return redirect('/')
        else:
            noactive = ' (no active)'


    if obj.user != request.user:
        reader = Readers()
        try:
            reader.user = request.user
        except:
            pass
        reader.ip = str(get_client_ip(request))
        reader.playcast = obj
        reader.date = datetime.datetime.now()
        reader.save()
    author=''
    if obj.user == request.user:

        author = '<a href="/designer/'+str(id)+'/"><button class="btn-editor">Edite</button></a><button class="btn-editor-del" onclick="DelQuest()">Delete</button><button class="btn-editor" onclick="Readers('+str(id)+');">Readers</button>'

    d = {'p':obj,'author':author,'tid':id,'noactive':noactive}
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
        a = str(request.POST['active'])
        if a == "false":
            obj.active = False;#
        else:
            obj.active = True
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
        st = st.replace('<script type="text/javascript" src="/static/js/ui/jquery.ui.mouse.js"></script>','')
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
        path = '/home/playcards/playcast/media/screen/'
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

            resault = '<head><script src="//code.jquery.com/jquery-1.9.1.js'+'"></script>'
            resault = resault + '<script src="/static/js/edite.js'+'"></script></head><body>'
            resault = resault + '<body onload="EndUploadMusic('+"'"+"'"+');'+'">OK</body>'
            return HttpResponse(resault)

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

def images_list(request,arg=0):

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
        links = ''
        if int(arg) > 9:
            links = '<button onclick="refresh('+str(int(arg)-10)+');">Previos </button>'

        if len(Picture.objects.all()) > (int(arg)+10):
            links = links + '<button onclick="refresh('+str(int(arg)+10)+');">Next </button>'
        d = {'L':L[0+arg:10+arg],'links':links}
        t = get_template("imageslist.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)




    for i in list:
        obj = Img()
        obj.url = '/media/'+ str(i.image)
        obj.width = str(102* i.image.width/i.image.height)
        L.append(obj)
    links = ''
    if int(arg) > 9:
        links = '<button onclick="refresh('+str(int(arg)-10)+');">Previos </button>'

    if len(Picture.objects.all()) > (int(arg)+10):
        links = links + '<button onclick="refresh('+str(int(arg)+10)+');">Next </button>'

    d = {'L':L[0+int(arg):10+int(arg)],'links':links}
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
            image = form.cleaned_data['file']
            if image:
                if image._size > 1024*1024:
                    return HttpResponse("Image file too large ( > 1M )")

            obj.image = image
            obj.key_words = form.cleaned_data['key_words'].lower()
            obj.user = request.user
            obj.datetime = datetime.datetime.now()
            obj.save()

            resault = '<head><script src="//code.jquery.com/jquery-1.9.1.js'+'"></script>'
            resault = resault + '<script src="/static/js/edite.js'+'"></script></head><body>'
            resault = resault + '<body onload="EndUploadImage('+"'"+"'"+');'+'">OK</body>'

            return HttpResponse(resault)
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
                if obj.active:
                    active = 'checked'
                else:
                    active = ''

    else:
        active = 'checked'
    d= {'active':active,'tid':tid,'title':title,'tbody':tbody,'tstyle':tstyle,'twidth':twidth,'theight':theight,'tmtitle':tmtitle,'tmurl':tmurl,'tmauthor':tmauthor,'tmperformer':tmperformer,'tcomment':tcomment}
    t = get_template("designer.html")
    c = Context(d)
    html = t.render(c)
   # response = HttpResponse(html)
#    response['Cache-Control'] = 'no-cache'
    return HttpResponse(html)

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