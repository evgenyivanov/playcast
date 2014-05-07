from django import forms

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