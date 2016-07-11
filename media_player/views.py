from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from media_browser.models import AudioTrack

import datetime
import os
import pyglet



def hello(request):
	return HttpResponse("Hello World")

def homepage_view(request):
	return HttpResponse("This is the homepage")

def current_datetime(request):
	now = datetime.datetime.now()
	#html = "<html><body>The time now is %s.</body></html>" % now
	#return HttpResponse(html)
	t = get_template('current_datetime.html')
	html = t.render(Context({'current_date': now}))
	return HttpResponse(html)


def video_player(request):
	t = get_template('video_player.html')
	html = t.render()
	return HttpResponse(html)

''' This function will render a media browser with all files in the media folder. '''
def media_browser(request):
	t = get_template('media_browser.html')

	# Obtain a list of all media files in the media folder.
	loaded_files = obtain_all_media_filenames()

	# Update the database with all the current media files found in the media folder.
 	update_media_library(loaded_files)

 	# Obtain all the values from the database
	audio_track_list = AudioTrack.objects.all()


	print("Audio Tracks: " + str(audio_track_list))

	html = t.render(Context({'loaded_files': loaded_files}))
	return HttpResponse(html)




def obtain_all_media_filenames():
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

	print(MEDIA_ROOT)

	loaded_files = []
	num_of_files = 0

	for filename in os.listdir(os.getcwd() + "/media/"):
		num_of_files+=1
		loaded_files.append(filename)
		print(filename)

	print("Total: " + str(loaded_files) + " " + str(num_of_files))

	return loaded_files


def update_media_library(filelist):
	for audio_track in filelist:
		track = AudioTrack(song_title = audio_track)
		print("Audio Track Title: " + str(track))

