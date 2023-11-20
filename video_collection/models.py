from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True) # allow for blank and null
    video_id = models.CharField(max_length=40, unique=True) # make sure user doesn't enter the same video

    def save(self, *args, **kwargs): # overwrite django's save method
        
        # extract video id from youtube url
        if not self.url.startswith('https://www.youtube.com/watch'): # checks that url is youtube
            raise ValidationError(f'Invalid YouTube URL {self.url}')

        url_components = parse.urlparse(self.url)
        query_string = url_components.query # string will include v query string
        if not query_string: # raise exception if there is no query string
            raise ValidationError(f'Invalid YouTube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True) # turn query string into dictionary
        v_parameters_list = parameters.get('v') # will return None if no key found, find v key 
        if not v_parameters_list: # checking if None or empty list
            raise ValidationError(f'Invalid YouTube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0] # string

        super().save(*args, **kwargs) # calls django's original save function


    def __str__(self): # string method
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id} ,Notes: {self.notes[:200]}'
