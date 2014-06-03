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
from models import *
import os, re
from PIL import Image
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.core.exceptions import ValidationError
from capcha import capthaGenerate
import hashlib
import numpy as np
from datetime import timedelta
#import urllib
from django.db.models import Count, Min, Sum, Avg


def browsers(request):
    browser = str(request.META['HTTP_USER_AGENT'])
    if browser.find('Chrome')==-1 and  browser.find('Safari')==-1 and browser.find('Opera')==-1 and browser.find('FireFox')==-1:
        d={}
        t = get_template("browsers.html")
        c = Context(d)
        html = t.render(c)
        return html
    else:
        return ''

def myjs(request):

    browser = str(request.META['HTTP_USER_AGENT'])
    brw = 'other'
    if browser.find('Chrome')>-1 or browser.find('Opera')>-1  or browser.find('Safari')>-1:
        d= {'Transform':'webkitTransform','cssTransform':'-webkit-transform'}
    elif browser.find('Firefox')>-1:
        d= {'Transform':'MozTransform','cssTransform':'-moz-transform'}
    elif browser.find('Trident')>-1:
        d= {'Transform':'msTransform','cssTransform':'-ms-transform'}
    else:
        d={}


    t = get_template("myjs.js")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def authors(request):
    L = list(User.objects.all().order_by('last_name','first_name'))
    d = {'L':L}
    t = get_template("authors.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


############################################################################

def account(request):
    list = Account.objects.filter(user = request.user).order_by('-date')
    balance = 0

    L=[]
    for i in list:
        L.append(i)
        balance = balance + i.sum
    d = {'user': request.user,'balance':balance,'L':L}
    t = get_template("account.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)


def credited(request):
    if not request.user.is_superuser:
        return redirect('/designer/')

    if request.method == 'POST':
        obj = Account()
        obj.date = datetime.datetime.now()
        obj.sum = int(request.POST['sum'])
        obj.text = request.POST['text']
        obj.user = User.objects.get(id = request.POST['user'])
        obj.save()
        return HttpResponse('OK')


    else:
        f = CreditedForm()
        d = {'f': f}
        d.update(csrf(request))
        t = get_template("credited.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)




def sendgift(request,id):
    if request.method == 'POST':
        user = User.objects.get(id = id)
        if user == None:
            return HttpResponse('<span style="color: red;">Error: user not found</span>')
        balance = 0
        l = Account.objects.filter(user = request.user)
        for i in l:
           balance = balance + i.sum
        gift = Gifts.objects.get(id = request.POST['gift'])
        if balance < gift.price:
             return HttpResponse('<span style="color: red;">Error: balance is '+str(balance)+'</span>')
        obj = SendGifts()
        obj.tuser = id
        obj.fuser = request.user.id
        obj.gift = gift
        obj.price = gift.price
        obj.date = datetime.datetime.now()+datetime.timedelta(days = gift.period)
        obj.save()

        obj=Account()
        obj.date = datetime.datetime.now()
        obj.sum = -1*gift.price
        obj.text = gift.title + ' to '+ user.username
        obj.user = request.user
        obj.save()

        return HttpResponse('OK')



    if request.method == 'GET':
        tuser = User.objects.get(id = id)
        balance = 0
        l = Account.objects.filter(user = request.user)
        for i in l:
           balance = balance + i.sum

        L = list(Gifts.objects.all())
        d = {'tuser': tuser,'balance':balance,'L':L,'id':id}
        d.update(csrf(request))
        t = get_template("sendgift.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)



@csrf_exempt
def loginza(request):
    if request.method == 'POST':
        token = request.POST.get('token', None)
        if token is None:
            return http.HttpResponseBadRequest()
        #f = urllib.urlopen('http://loginza.ru/api/authinfo?token=%s' % token)
        #result = f.read()
        #f.close()
        return HttpResponse(token)

    if request.method == 'GET':
        d = {}
        t = get_template("loginza.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)

def about(request):
    d = {}
    t = get_template("about.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def login2(request):


    if request.method == 'POST': # If the form has been submitted...

        f = LoginForm(request.POST)
        login_ = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=login_, password=password)

        if  user is not None:
            login(request, user)
            return redirect('/designer/')
        else:

             d = {'f': f,'errors':'Error: login and password'}
             d.update(csrf(request))
             t = get_template("login.html")
             c = Context(d)
             html = t.render(c)
             return HttpResponse(html)

    else:

        f = LoginForm
        d = {'f': f}
        d.update(csrf(request))
        t = get_template("login.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)


def register(request):

    captcha=  capthaGenerate(request)
    mm = hashlib.md5()
    mm.update(captcha[1])

    if request.method == 'POST':
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
            new_user.first_name= formUser.cleaned_data['first_name'],
            new_user.last_name= formUser.cleaned_data['last_name'],
            new_user.save()
            new_user.first_name = str(new_user.first_name).replace("(u'","").replace("',)","")
            new_user.last_name = str(new_user.last_name).replace("(u'","").replace("(u'","").replace("',)","")
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
        L = list(Readers.objects.filter(playcast = playcast))
        total=len(L)
        d = {'L':L,'id':id,'title': playcast.title,'total': total}
        t = get_template("readers.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)
    return HttpResponse('You is not author')


def author(request,id):
    usr = User.objects.get(id = id)
    if len(UserProfile.objects.filter(user = usr))==0:
        obj = UserProfile()
        obj.user = usr
        obj.save()
        profile = obj
    else:
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
    presents = []
    list = SendGifts.objects.filter(tuser = id)
    now = datetime.datetime.now()
    for i in list:
        if i.date > now:
            presents.append(i)
    controls = ""
    if str(request.user.id) == str(id):
        controls = '<button  class="btn-editor" onclick = "Account();">Account</button>'
    else:
        if str(request.user) != 'AnonymousUser':
            controls = '<button  class="btn-editor" onclick = "SendPresent();">Send present</button>'
    d = {'user':usr,'p':profile,'L':L,'url_img':url_img,'h':h,'presents':presents,'controls':controls}
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

    delta = datetime.datetime.now()-timedelta(minutes=15)

    NonStop2 = True
    ip = str(get_client_ip(request))
    list_error = LoginError.objects.filter(ip = ip).order_by('-date')

    if len(list_error)>5:

        if list_error[4].date > delta:
            NonStop2 = False



    if user is not None and NonStop2:
        if user.is_active:
            login(request, user)
            html = 'Hello, <a href="/author/'+str(user.id)+'/" target = "_blank'+'">'+user.first_name+' '+user.last_name+'</a>!<br />'
            html = html + '<button onclick="EditeProfile();" >' +'Edite profile'+'</button>'
            html = html +'<button type="button" onclick="document.location.href='
            html = html + "'/accounts/logout/?next=/';"
            html = html +'">'+'Log out'+'</button>'

        else:
            pass
    else:
        if NonStop2 == False:
            errors ="Plese, try again later (~15 minut)"
        else:
            err = LoginError()
            err.date = datetime.datetime.now()
            err.ip = get_client_ip(request)
            err.save()
            errors= "Error: login and password"

        html = '<span style="color: red;'+'">'+errors+'</span>'
        html = html + '<br />login <span style="position:relative;left:29px;"><input type="text" id ="login" value=""></span>'
        html = html +'password <input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button>'+'or'+' <a href="/register">'+'Sign up'+'</a>'




    return HttpResponse(html)

def CurrentUser(request):

    user = request.user
    if str(user) == 'AnonymousUser':
        html = 'Hello, Guest!'+'<br />login <span style="position:relative;left:29px;"><input type="text" id ="login" value=""></span>'
        html = html +'password'+ '<input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button> ' +'or'+' <a href="/register">'+'Sign up'+'</a>'
    else:
        html = 'Hello'+', <a href="/author/'+str(user.id)+'/" target = "_blank'+'">'
        html = html +  user.first_name+' ' + user.last_name
        html = html+ '</a>!<br />'
        html = html + '<button onclick="EditeProfile();" >'+'Edite profile'+'</button>'
        html = html +'<button type="button" onclick="logout();">'+'Log out'+'</button>'
    return HttpResponse(html)

def home(request):

    user = request.user
    if str(user) == 'AnonymousUser':
        html = 'Hello, Guest!'+'<br />login <span style="position:relative;left:29px;"><input type="text" id ="login" value=""></span>'
        html = html +'password' +'<input type="password" id = "password" value="">'
        html = html +'<button type="button" onclick="LogIn();">OK</button>'+ 'or' +'<a href="/register">'+'Sign up'+'</a>'
    else:
        html = 'Hello'+', <a href="/author/'+str(user.id)+'/" target = "_blank'+'">'
        html = html +  user.first_name+' ' + user.last_name
        html = html+ '</a>!<br />'
        html = html + '<button onclick="EditeProfile();" >' + 'Edite profile' + '</button>'
        html = html +'<button type="button" onclick="logout();">'+ 'Log out'+ '</button>'
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
        links = '<a href = /playcast_list/'+str(int(arg)-10)+'/><Previos</a>  '
    if len(Playcast.objects.all()) > (int(arg)+10):
        links = links + '<a href = /playcast_list/'+str(int(arg)+10)+'/>Next ></a>'
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
        return redirect('/author/'+str(request.user.id)+'/')

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
    cnt = len(Readers.objects.filter(playcast = obj))

    if (cnt//50) == (float(cnt)/50) and cnt>0:
        ac = Account()
        ac.date= datetime.datetime.now()
        ac.sum = 1
        ac.text = obj.title
        ac.user = obj.user
        ac.save()
    author=''
    if obj.user == request.user:
        author = '<a href="/designer/'+str(id)+'/"><button class="btn-editor">'+"Edite"+'</button></a><button class="btn-editor-del" onclick="DelQuest();">'+"Delete"+'</button><button class="btn-editor" onclick="Readers('+str(id)+');">'+'Readers'+'</button>'
    profile = UserProfile.objects.filter(id = obj.user.id)[0]
    try:
        url = profile.photo.url
    except:
        url='/static/images/no_image.gif'

    browser = str(request.META['HTTP_USER_AGENT'])
    body = obj.body
    if browser.find('Chrome')>-1 or  browser.find('Safari')>-1 or browser.find('Opera')>-1:
        #body = body.replace(' transform:',' -webkit-transform:')
        body = body.replace('-moz-transform:','-webkit-transform:')
        body = body.replace(' transform:','-webkit-transform:')
    elif browser.find('Firefox')>-1:
        body = body.replace('-webkit-transform:','-moz-transform:')
        body = body.replace(' transform:','-moz-transform:')
   # elif browser.find('Trident')>-1:
    #    body = body.replace(' -webkit-transform:'," -ms-transform:")
     #   body = body.replace(' -moz-transform:'," -ms-transform:")

    d = {'p':obj,'author':author,'tid':id,'noactive':noactive,'url':url,'body':body}
    t = get_template("playcast.html")
    c = Context(d)
    html = browsers(request)+t.render(c)
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
        st = st.replace('<div class="ui-resizeble-handle ui-resizeble-ne" unselecttable="on" style="z-index:1001;"></div>','')
        st = st.replace('<div class="ui-resizeble-handle ui-resizeble-nw" unselecttable="on" style="z-index:1002;"></div>','')
        st = st.replace('<div class="ui-resizeble-handle ui-resizable-se ui-icon ui-icon-gripsmall-diagonal-se" unselecttable="on" style="z-index:1003;" <="" div=""><div class="ui-resizeble-handle ui-resizeble-sw" unselecttable="on" style="z-index:1004;"></div></div>','')

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
        obj.comment = request.POST['comments']
        obj.save()
        return HttpResponse(obj.id)




@csrf_exempt
def save(request):

    if request.method == "POST":

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

        data = np.array(img)
        x = len(data[:,1])-1
        y = len(data[1,:]) -1




        r = 0
        g= 0
        b = 0
        n = 0

        for i in range(x):
            for j in range(y):
                n = n + 1
                r = r + data[i][j][0]
                g = g + data[i][j][1]
                b = b + data[i][j][2]
        r = r //(x*y)
        g =  g // (x*y)
        b =  b //(x*y)

        color1='('+str(r)+','+str(g)+','+str(b)+')'
        for i in range(x):
            for j in range(4):
                data[i][j][0]= r
                data[i][j][1]= g
                data[i][j][2]= b
                data[i][j-3+y][0]= r
                data[i][j-3+y][1]= g
                data[i][j-3+y][2]= b

        for j in range(y):
            for i in range(4):
                data[i][j][0]= r
                data[i][j][1]= g
                data[i][j][2]= b
                data[x-3+i][j][0]= r
                data[x-3+i][j][1]= g
                data[x-3+i][j][2]= b
        size = 420, 420
        img.thumbnail(size, Image.ANTIALIAS)
        im = Image.fromarray(data)
        im.save(path,"JPEG")


        r = 255 - r
        g = 255 - g
        b = 255 - b
        if r > 100 and r < 200:
            r = 255
        if g > 100 and g < 200:
            g = 255
        if b > 100 and b < 200:
            b = 255


        color2='('+str(r)+','+str(g)+','+str(b)+')'

        color3='(0,0,0)'

        obj = Playcast.objects.get(id = str(request.POST['id']))
        obj.color1 = color1;
        obj.color2 = color2;
        obj.color3 = color3;
        obj.save()

        return HttpResponse(path)

def select_music(request):
    d = {}
    t = get_template("selectmusic.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def music_list(request,arg=0):
    L=[]

    if str(request.GET['my']) == 'true':
        list = Music.objects.filter(user = request.user).order_by('-datetime')
    else:
        list = Music.objects.all().order_by('-datetime')


    #keywords = request.GET['words'].lower()
    #if len(keywords) > 0:
    #    keys = keywords.split()
    #    S= set()
    #    for i in keys:
    #        songs = list.filter(mtitles__contains = i)
    #        for j in songs:
    #            S.add(j)

    #    L=[]
    #    for i in S:
    #        L.append(i)
    #    links = ''
    #    if int(arg) > 9:
    #        links = '<button onclick="refresh('+str(int(arg)-10)+');"><Previos </button>'

     #   if len(Picture.objects.all()) > (int(arg)+10):
     #       links = links + '<button onclick="refresh('+str(int(arg)+10)+');">Next> </button>'
     #   d = {'L':L[0+arg:10+arg],'links':links}
     #   t = get_template("musiclist.html")
     #   c = Context(d)
      #  html = t.render(c)
       # return HttpResponse(html)




    for i in list:
       L.append(i)
    links = ''
    d = {'L':L[0+int(arg):10+int(arg)],'links':links}
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

        for i in keys:
            S = set(list(list.filter(key_words__contains = i)))


        L=[]
        for i in S:
            obj = Img()
            obj.url = '/media/'+ str(i.image)
            obj.width = str(102* i.image.width/i.image.height)
            obj.w = i.image.width
            obj.h = i.image.height
            L.append(obj)
        links = ''
        if int(arg) > 9:
            links = '<button onclick="refresh('+str(int(arg)-10)+');">  Previos </button>'

        if len(Picture.objects.all()) > (int(arg)+10):
            links = links + '<button onclick="refresh('+str(int(arg)+10)+');"> Next></button>'
        d = {'L':L[0+arg:10+arg],'links':links}
        t = get_template("imageslist.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)




    for i in list:
        obj = Img()
        obj.url = '/media/'+ str(i.image)
        obj.width = str(102* i.image.width/i.image.height)
        obj.w = i.image.width
        obj.h = i.image.height
        L.append(obj)
    links = ''
    if int(arg) > 9:
        links = '<button onclick="refresh('+str(int(arg)-10)+');"> Previos </button>'

    if len(Picture.objects.all()) > (int(arg)+10):
        links = links + '<button onclick="refresh('+str(int(arg)+10)+');">Next> </button>'

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
                if image._size > 1.5*1024*1024:
                    return HttpResponse("Image file too large ( > 1.5M )")

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
    tstyle = 'background-color:#FFFFB5;'
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
                browser = str(request.META['HTTP_USER_AGENT'])
                if browser.find('Chrome')>-1 or  browser.find('Safari')>-1 or browser.find('Opera')>-1:
                    tbody = tbody.replace(' transform:',' -webkit-transform:')
                    tbody = tbody.replace('-moz-transform:','-webkit-transform:')
                    tbody = tbody.replace('-ms-transform:','-webkit-transform:')
                elif browser.find('Firefox')>-1:
                    tbody = tbody.replace(' transform:',' -moz-transform:')
                    tbody = tbody.replace('-webkit-transform:','-moz-transform:')
                    tbody = tbody.replace('-ms-transform:','-moz-transform:')
               # elif browser.find('Trident')>-1:
                #    tbody = tbody.replace(' -webkit-transform:'," -ms-transform:")
                 #   tbody = tbody.replace(' -moz-transform:'," -ms-transform:")


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
    html = browsers(request)+t.render(c)

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