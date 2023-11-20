from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import VideoForm, SearchForm
from .models import Video

def home(request): # home view function
    app_name = 'Football Videos' # name of category
    return render(request, 'video_collection/home.html', {'app_name':app_name}) # renders home page

def add(request): # add view function
    
    if request.method == 'POST': # if POST, creating new video
        new_video_form = VideoForm(request.POST) # use the data that was sent by post request
        if new_video_form.is_valid(): # check if user has enter filled in all required data
            try:
                new_video_form.save() # save form data to DB
                return redirect('video_list') # redirect to list of videos
                # messages.info(request, 'New video saved!') # success message

            except ValidationError: # invalid url
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError: # duplicates
                messages.warning(request, 'You already added this YouTube Video')

        messages.warning(request, 'Please check the data entered.')
        # redisplay add.html and display the data the user typed so they can edit the data
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

def video_list(request):

    search_form = SearchForm(request.GET) # build the form from data use sent to program
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term'] # example: 'vikings' or 'lose' 
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) # checks if video contains search term and order by name in lowercase
    
    else: # form is not filled or this is the first time user sees the page
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name')) # get data from Video model in the order of name in lowercase
    
    return render(request, 'video_collection/video_list.html', {'videos':videos, 'search_form': search_form})