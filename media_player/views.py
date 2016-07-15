from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from media_browser.models import AudioTrack
from django.shortcuts import get_object_or_404

import datetime
import os
import id3reader
import string

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
	html = t.render({'current_date': now})
	return HttpResponse(html)

def video_player(request):
	t = get_template('video_player.html')
	html = t.render()
	return HttpResponse(html)

def canvas_video(request):
	t = get_template('canvas_sandbox.html')
	html = t.render()
	return HttpResponse(html)

def trailers(request):
	t = get_template('trailers.html')

	listing_of_files, num_of_files = obtain_all_video_filenames()

	print(listing_of_files, num_of_files)

	html = t.render({'number_of_files': num_of_files})
	html = t.render({'list_of_files': listing_of_files})

	return HttpResponse(html)	

def obtain_all_video_filenames():
	''' This function will obtain a list of all video files in the media folder. '''
	print("----------------------------------------------------------------")
	print("Obtaining all video file_names")
	if(VERBOSE):
		print("\nMEDIA DIRECTORY: " + MEDIA_ROOT)

	loaded_files = []
	num_of_files = 0

	# Iterate over all files found in the media directory. Count the total number of files.
	for filename in os.listdir(os.getcwd() + "/media/"):
		if(VERBOSE):
			print(filename)
		if(filename.endswith(".mp4") or filename.endswith(".ogg") or filename.endswith(".webm") or filename.endswith(".ogv")):
			num_of_files+=1
			loaded_files.append(filename)

	return loaded_files, num_of_files


def media_browser(request):
	''' This function will render a media browser with all files in the media folder. '''
	t = get_template('media_browser.html')

	# Provides a list of file_names.
	found_files = obtain_all_media_filenames()

	# Checks the found files for 
	new_files = scan_for_new_audio_files()

	if(len(new_files) > 0):
		print("New files were found.")
		# Update the database with all the current media files found in the media folder.
 		for new_file in new_files:
 			print("Adding " + new_file)
 			write_ID3_tag_information_to_database(new_file)

	else:
		print("No new files.")
		
	audio_track_list = AudioTrack.objects.all()

	# Swap out the files found to be substituted and rendered into the HTML.
	html = t.render({'loaded_files': audio_track_list})

	return HttpResponse(html)


def scan_for_new_audio_files():
	print("---------Scanning---for-----new------files----------------")
	# Obtain a list of all media files in the media folder.
	loaded_files, num_of_files = obtain_all_media_filenames()

	# Obtain all objects from the database
	audio_track_list = AudioTrack.objects.all()

	# Output how many files are found in both the database and media folder.
	if(VERBOSE):
		print(str(num_of_files) + " :number of files in the media directory. \n")
		print(str(audio_track_list) + " :number of files in database. \n")

	# If we have the same count or more files in the database, don't load any more.
	if (len(audio_track_list) >= len(loaded_files)):
		return []

	# If the database is empty, load all files in the media folder.
	if (len(audio_track_list) == 0):
		print("No audio tracks in the database")
		return loaded_files

	# Output all files in the media folder.
	for audio_file in loaded_files:
		print("Audio File")
		print(audio_file)

	# Output all files in the database.
	for track in audio_track_list:
		print("Audio Track")
		print(track.file_name)

	# Iterate through all audio files in the database, if the filename matches
	# a filename matched in the media folder, remove it from the list of 
	# tracks to be added.
	for database_file in audio_track_list:
		if(database_file in loaded_files):
			loaded_files.remove(database_file)

	return loaded_files

	print("---------Done-------------------Scanning----------------")
	return loaded_files


def write_ID3_tag_information_to_database(current_audio_track):
	''' This function will obtain individual ID3 tags from an MP3 file and save it to the AudioTrack
	Django Model if the value is non-null. '''
	# Initialize all fields to an empty string.
	album = ""
	performer = ""
	title = ""
	year = ""
	genre = ""
	track_number = ""
	performer = ""
	song_title = ""

	# Obtain the media diretory with the current media file in order to read the ID3 tags.
	id3r = id3reader.Reader(MEDIA_ROOT + current_audio_track)

	# If each ID3 tag is not null, write it to the database row entry.
	if(id3r.getValue('album') != None):
		album = str(id3r.getValue('album').encode("utf-8"))
	if(id3r.getValue('performer') != None):
		performer = str(id3r.getValue('performer'))
	if(id3r.getValue('title') != None):
		song_title = str(id3r.getValue('title').encode("utf-8"))
	if(id3r.getValue('year') != "" and id3r.getValue('year') != None):
		year = str(id3r.getValue('year').encode("utf-8"))
	if(id3r.getValue('genre') != None and id3r.getValue('genre') != ""):
		genre = str(id3r.getValue('genre').encode("utf-8"))
	if(id3r.getValue('track') != "" and id3r.getValue('track') != None):
		track_number = str(id3r.getValue('track').encode("utf-8"))

	audio_track_object = AudioTrack(file_name = str(current_audio_track), song_title=str(song_title), artist=str(performer), album=str(album), genre=genre, year=year, track_number=track_number)

	audio_track_object.save()

	# Save all fields for this database row entry.
	return audio_track_object



def obtain_all_media_filenames():
	''' This function will obtain a list of all files in the media folder. '''
	print("----------------------------------------------------------------")
	print("Obtaining all media file_names")
	if(VERBOSE):
		print("\nMEDIA DIRECTORY: " + MEDIA_ROOT)

	loaded_files = []
	num_of_files = 0

	# Iterate over all files found in the media directory. Count the total number of files.
	for filename in os.listdir(os.getcwd() + "/media/"):
		if(VERBOSE):
			print(filename)
		if(filename.endswith(".mp3")):
			num_of_files+=1
			loaded_files.append(filename)

	return loaded_files, num_of_files

def clean(instr):
    return instr.translate(None, string.punctuation + '')


def parse_RSS_feed(url):


	pass
