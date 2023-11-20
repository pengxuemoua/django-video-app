from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    # list the fields from the Video model
    class Meta:
        model = Video 
        fields = ['name', 'url', 'notes'] # put fields from Video model into a list