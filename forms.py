from django import forms

class RegUserForm(forms.Form):
    username = forms.CharField(label='Name',max_length=100)
    first_name = forms.CharField(label='Name',max_length=100)
    last_name = forms.CharField(label='Name',max_length=100)
    email = forms.EmailField(label='E-mail')
    passw1 = forms.CharField(label='password',min_length=6,max_length=32, widget=forms.PasswordInput)
    passw2 = forms.CharField(label='re-password',min_length=6,max_length=32, widget=forms.PasswordInput)


class UserForm(forms.Form):
    first_name = forms.CharField(label='Name',max_length=100)
    last_name = forms.CharField(label='Name',max_length=100)
    email = forms.EmailField()


class UserProFileForm(forms.Form):
    photo = forms.FileField(label='photo')
    url = forms.URLField( )
    about = forms.CharField(widget=forms.Textarea)

class UploadImageForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    name = forms.CharField(label='Name',max_length=100)
    file  = forms.FileField(label='picture')
    key_words = forms.CharField(label='Key words use space',max_length=200)


class UploadMusicForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    title = forms.CharField(label='Name',max_length=100)
    file  = forms.FileField(label='picture')
    author = forms.CharField(label='Author',max_length=200)
    performer = forms.CharField(label='Performer',max_length=200)
    key_words = forms.CharField(label='Key words use space',max_length=200)