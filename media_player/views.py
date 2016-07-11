from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from media_browser.models import AudioTrack

import datetime
import os
import id3reader

VERBOSE = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

def hello(request):
	return HttpResponse("Hello World")

def homepage_view(request):
	return HttpResponse("This is the homepage")

def current_datetime(request):
	now = datetime.datetime.now()
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
	print("LIST: " + str(audio_track_list))

	# Swap out the files found to be substituted and rendered into the HTML.
	html = t.render(Context({'loaded_files': loaded_files}))
	return HttpResponse(html)


def obtain_all_media_filenames():
	if(VERBOSE):
		print("MEDIA DIRECTORY: " + MEDIA_ROOT)

	loaded_files = []
	num_of_files = 0

	# Iterate over all files found in the media directory. Count the total number of files.
	for filename in os.listdir(os.getcwd() + "/media/"):
		if(VERBOSE):
			print(filename)
		num_of_files+=1
		loaded_files.append(filename)

	if(VERBOSE):
		print("Total: " + str(loaded_files) + " " + str(num_of_files))

	return loaded_files


def obtain_ID3_tag_information(audio_track, audio_track_object):
	# Initialize all fields to an empty string.
	album = ""
	performer = ""
	title = ""
	track = ""
	year = ""
	genre = ""
	track_number = ""
	artist = ""
	comment = ""
	copyright = ""

	# Obtain the media diretory with the current media file in order to read the ID3 tags.
	id3r = id3reader.Reader(MEDIA_ROOT + audio_track)

	if (VERBOSE):
		print("-----Starting ID3 Process-------")
		print(id3r.getValue('album'))
		print(id3r.getValue('performer'))
		print(id3r.getValue('title'))
		print(id3r.getValue('track'))
		print(id3r.getValue('year'))
		print(id3r.getValue('genre'))
		print(id3r.getValue('track number'))
		print(id3r.getValue('artist'))
		print(id3r.getValue('comment'))
		print(id3r.getValue('copyright'))
		print("-----------Ending---------------")

	# If each ID3 tag is not null, write it to the database row entry.
	if(id3r.getValue('album') != None):
		audio_track_object.album = id3r.getValue('album')
	if(id3r.getValue('performer') != None):
		audio_track_object.performer = id3r.getValue('performer')
	if(id3r.getValue('title') != None):
		audio_track_object.title = id3r.getValue('title')
	if(id3r.getValue('track') != None):
		audio_track_object.track = id3r.getValue('track')
	if(id3r.getValue('year') != None):
		audio_track_object.year = id3r.getValue('year')
	if(id3r.getValue('genre') != None):
		audio_track_object.genre = id3r.getValue('genre')
	if(id3r.getValue('track number') != None):
		audio_track_object.track_number = id3r.getValue('track number')
	if(id3r.getValue('artist') != None):
		audio_track_object.artist = id3r.getValue('artist')
	if(id3r.getValue('comment') != None):
		audio_track_object.comment = id3r.getValue('comment')
	if(id3r.getValue('copyright') != None):
		audio_track_object.copyright = id3r.getValue('copyright')

	# Save all fields for this database row entry.
	audio_track_object.save()


def update_media_library(filelist):
	for audio_track in filelist:
		# Initialize an audio track database entry with only the file name.
		track = AudioTrack(song_title = audio_track)

		# Set the remaining ID3 tag values into the database row entry.
		obtain_ID3_tag_information(audio_track, track)



