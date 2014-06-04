# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


class CreditedForm(forms.Form):

    sum = forms.IntegerField(required=True)
    text = forms.CharField(max_length=200)
    user = forms.ModelMultipleChoiceField(queryset=User.objects.all())

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField( widget=forms.PasswordInput)

class RegUserForm(forms.Form):
    username = forms.CharField(label= 'Имя',max_length=100)
    first_name = forms.CharField(label= 'Имя',max_length=100)
    last_name = forms.CharField(label= 'Имя',max_length=100)
    email = forms.EmailField(label='E-mail')
    passw1 = forms.CharField(label= 'пароль',min_length=6,max_length=32, widget=forms.PasswordInput)
    passw2 = forms.CharField(label= 'повторить',min_length=6,max_length=32, widget=forms.PasswordInput)


class UserForm(forms.Form):
    first_name = forms.CharField(label= 'Имя',max_length=100)
    last_name = forms.CharField(label= 'Имя' ,max_length=100)
    email = forms.EmailField()


class UserProFileForm(forms.Form):
    photo = forms.FileField(label='photo')
    url = forms.URLField( )
    about = forms.CharField(widget=forms.Textarea)

class UploadImageForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    name = forms.CharField(label='Имя',max_length=100)
    file  = forms.FileField(label='Изображение')
    key_words = forms.CharField(label='Ключевые слова',max_length=200)


class UploadMusicForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    title = forms.CharField(label='Название',max_length=100)
    file  = forms.FileField(label='Файл')
    author = forms.CharField(label='Автор',max_length=200)
    performer = forms.CharField(label='Исполнитель',max_length=200)
    key_words = forms.CharField(label='Ключевые слова',max_length=200)