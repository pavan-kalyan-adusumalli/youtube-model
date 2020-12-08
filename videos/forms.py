from django import forms
from .models import Video, Channel

class AddChannelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    portfolio = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    fblink = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    twitterlink = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    instalink = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'aria-describedby':'basic-addon1'}))
    class Meta:
        model = Channel
        fields = ['owner', 'channelname', 'channelpicture', 'description', 'portfolio', 'fblink', 'twitterlink', 'instalink']

class AddVideoForm(forms.ModelForm):
    videoname = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Add a title that describes your video'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Tell viewers about your video'}))
    subtitles = forms.FileField(required=False)
    class Meta:
        model = Video
        fields = ['videoname', 'thumbnail', 'recording', 'subtitles', 'description', 'category', 'uploadedchannel', 'hideComments']
