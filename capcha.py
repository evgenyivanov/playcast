from hashlib import md5
from PIL import Image, ImageDraw, ImageFont
import random
from StringIO import StringIO
import os

def capthaGenerate(request):
    path=os.path.join(os.path.dirname(__file__), 'fonts').replace('\\','/')
    path=os.path.join(path, 'BELL.TTF').replace('\\','/')
    #path = "/nginx/project/files/static/c/"
    im = Image.new('RGBA', (200, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    number = ""
    margin_left = 0
    margin_top = 0
    colorNUM = ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f")
    i = 0
    while (i < 6):
        font_color = "#"+str(random.randint(0,9))
        y = 0
        while (y < 5):
            rand = random.choice(colorNUM)
            font_color = font_color+rand
            y = y+1
        rand_x11 = random.randint(0,100)
        rand_x12 = random.randint(100,200)
        rand_y11 = random.randint(0,50)
        rand_y12 = random.randint(0,50)
        draw.line((rand_x11, rand_y11, rand_x12, rand_y12), fill="#a9a6a6")
        font_rand =str(random.randint(1,10))
        fontSize_rand =random.randint(30,40)
        font = ImageFont.truetype(path, fontSize_rand)
        b= random.randint(0,22)
        if (b - 13)>0:
            if (b-13)==1:
                a = "A"
            elif (b-13)==2:
                a = "B"
            elif (b-13)==3:
                a = "C"
            elif (b-13)==2:
                a = "B"
            elif (b-13)==4:
                a = "D"
            elif (b-13)==5:
                a = "E"
            elif (b-13)==6:
                a = "G"
            elif (b-13)==7:
                a = "H"
            elif (b-13)==8:
                a = "G"
            elif (b-13)==9:
                a = "I"
            elif (b-13)==10:
                a = "J"
            elif (b-13)==11:
                a = "K"
        else:
            a = str(b)

        draw.text((margin_left,margin_top), a,fill=str(font_color),font=font)
        rand_x11 = random.randint(0,100)
        rand_x12 = random.randint(100,200)
        rand_y11 = random.randint(0,50)
        rand_y12 = random.randint(0,50)
        draw.line((rand_x11, rand_y11, rand_x12, rand_y12), fill="#a9a6a6")
        margin_left = margin_left+random.randint(20,35)
        margin_top = random.randint(0,20)
        i = i+1
        number = number+a
    salt = "$@!SAf*$@)ASFfacnq==124-2542SFDQ!@$1512czvaRV"
    key = md5(str(number+salt)).hexdigest()
    output = StringIO()
    im.save(output, format="PNG")
    contents = output.getvalue().encode("base64").replace("\n", "")
    img_tag = '<img value="'+key+'" src="data:image/png;base64,{0}">'.format(contents)
    output.close()
    return [img_tag, number]