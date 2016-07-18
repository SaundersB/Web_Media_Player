from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from media_browser.models import AudioTrack, VideoTrack
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc

import datetime
import os
import id3reader
import string
import subprocess


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

def audio_media_browser(request):
	''' This function will render a media browser with all files in the media folder. '''
	t = get_template('audio_media_browser.html')

	# Provides a list of file_names.
	found_files = obtain_all_audio_filenames()

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


def video_media_browser(request):
	''' This function will render a media browser with all files in the media folder. '''
	t = get_template('video_media_browser.html')

	# Provides a list of file_names.
	found_files, num_of_files = obtain_all_video_filenames()

	new_files = scan_for_new_video_files()

	print(found_files)
	print(new_files)
	
	
	if(len(new_files) > 0):
		print("New files were found.")
		# Update the database with all the current media files found in the media folder.
		print(new_files)
 		for new_file in found_files:
 			print("Writing out video files")
 			print(new_file)
 			write_video_information_to_database(new_file)

	else:
		print("No new files.")

	video_track_list = VideoTrack.objects.all()
	

	
	# Swap out the files found to be substituted and rendered into the HTML.
	#html = t.render({'loaded_files': audio_track_list})
	#if(len(video_track_list) > 0):
	#	print("There are new files.")
	#	html = t.render({'loaded_files': new_files})
	#else:
	#	print("There are no files.")
	html = t.render({'loaded_files': video_track_list})

	return HttpResponse(html)


def scan_for_new_audio_files():
	print("---------Scanning---for-----new------files----------------")
	# Obtain a list of all media files in the media folder.
	loaded_files, num_of_files = obtain_all_audio_filenames()

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

	print("---------Done-------------------Scanning----------------")
	return loaded_files


def scan_for_new_video_files():
	print("---------Scanning---for-----new------files----------------")
	# Obtain a list of all media files in the media folder.
	loaded_files = obtain_all_video_filenames()

	# Obtain all objects from the database
	video_track_list = VideoTrack.objects.all()

	# If we have the same count or more files in the database, don't load any more.
	if (len(video_track_list) >= len(loaded_files)):
		return []

	# If the database is empty, load all files in the media folder.
	if (len(video_track_list) == 0):
		print("No video tracks in the database")
		return loaded_files

	# Output all files in the media folder.
	for video_file in loaded_files:
		print("Video File")
		print(video_file)

	# Output all files in the database.
	for track in video_track_list:
		print("Video Track")
		print(track.file_name)

	# Iterate through all audio files in the database, if the filename matches
	# a filename matched in the media folder, remove it from the list of 
	# tracks to be added.
	for database_file in video_track_list:
		if(database_file in loaded_files):
			loaded_files.remove(database_file)

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
	read_track_title = ""

	# Obtain the media diretory with the current media file in order to read the ID3 tags.
	id3r = id3reader.Reader(MEDIA_ROOT + current_audio_track)

	# If each ID3 tag is not null, write it to the database row entry.
	if(id3r.getValue('album') != None):
		album = str(id3r.getValue('album').encode("utf-8"))
		print("Album: " + album)
	if(id3r.getValue('performer') != None):
		performer = str(id3r.getValue('performer'))
		print("Artist: " + performer)
	if(id3r.getValue('title') != None):
		song_title = str(id3r.getValue('title').encode("utf-8"))
		print("Song Title: " + song_title)
	if(id3r.getValue('year') != "" and id3r.getValue('year') != None):
		year = str(id3r.getValue('year').encode("utf-8"))
		print("Year: " + year)
	if(id3r.getValue('genre') != None and id3r.getValue('genre') != ""):
		genre = str(id3r.getValue('genre').encode("utf-8"))
		print("Genre: " + genre)
	if(id3r.getValue('track') != "" and id3r.getValue('track') != None):
		track_number = str(id3r.getValue('track').encode("utf-8"))
		print("Track Number: " + track_number)

	read_track_title = current_audio_track.split(".")[0]

	audio_track_object = AudioTrack(file_name = str(current_audio_track), song_title=str(song_title), artist=str(performer), album=str(album), genre=str(genre), year=str(year), track_number=str(track_number), track_title=str(read_track_title))

	audio_track_object.save()

	# Save all fields for this database row entry.
	return audio_track_object


def write_video_information_to_database(current_video_track):
	''' This function will obtain individual ID3 tags from an MP3 file and save it to the AudioTrack
	Django Model if the value is non-null. '''
	# Initialize all fields to an empty string.
	read_video_title = ""
	read_video_length = ""
	read_video_width = ""
	read_video_height = ""
	read_video_aspect_ratio = ""
	read_video_frame_rate = ""
	read_video_format = ""
	read_bit_rate = ""
	read_artist = ""
	read_genre = ""
	read_play_count = ""
	read_rating = ""
	read_year = ""
	read_file_size = ""
	read_file_name = ""

	time_now = datetime.datetime.now()

	video_file_metadata = getVideoMetadata(current_video_track)


	print("-----------Video__" + current_video_track  + "__Metadata---------")

	data = getMediaInfoMetadata(current_video_track)

	for line in data:
		#print("Line: " + line)

		if 'Format  ' in line:
			print(line)
			read_video_format = line
			read_video_format = read_video_format.split(":")[1]
		if 'Duration' in line:
			print(line)
			read_video_length = line
			read_video_length = read_video_length.split(":")[1]

		if 'Overall bit rate' in line:
			print(line)
			read_bit_rate = line
			read_bit_rate = read_bit_rate.split(":")[1]

		if 'Width' in line:
			print(line)
			read_video_width = line
			read_video_width = read_video_width.split(":")[1]
			read_video_width = read_video_width.replace(' ', '')
			read_video_width = read_video_width.replace('pixels', '')

		if 'Height' in line:
			print(line)
			read_video_height = line
			read_video_height = read_video_height.split(":")[1]
			read_video_height = read_video_height.replace(' ','')
			read_video_height = read_video_height.replace('pixels','')

		if 'Display aspect ratio' in line:
			print(line)
			read_video_aspect_ratio = line
			read_video_aspect_ratio = read_video_aspect_ratio.split(":")[1] + ":" + read_video_aspect_ratio.split(":")[2]

		if 'Frame rate' in line:
			print(line)
			read_video_frame_rate = line
			read_video_frame_rate = read_video_frame_rate.split(":")[1]

		if 'File size' in line:
			print(line)
			read_file_size = line
			read_file_size = read_file_size.split(":")[1]

		if 'Encoded Date' in line:
			print(line)
			read_file_size = line
			read_file_size = read_file_size.split(":")[1]
	
	video_track_object = VideoTrack(file_name = str(current_video_track), video_title=str(read_video_title),\
		video_length=str(read_video_length), video_width=str(read_video_width),\
		video_height=str(read_video_height), video_aspect_ratio=str(read_video_aspect_ratio),\
		video_frame_rate=str(read_video_frame_rate), video_format=str(read_video_format),\
		bit_rate=str(read_bit_rate), file_size=str(read_file_size), rating="")

	video_track_object.save()

	# Save all fields for this database row entry.
	return video_track_object
	


def obtain_all_audio_filenames():
	''' This function will obtain a list of all audio files in the media folder. '''
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
		if(filename.endswith(".mp4") or filename.endswith(".ogg") or filename.endswith(".webm") or filename.endswith(".ogv") or filename.endswith(".mkv")):
			num_of_files+=1
			loaded_files.append(filename)

			if(VERBOSE):
				print(filename)

	print("Loaded Video Files:")
	print(loaded_files)
	print("\n")

	return loaded_files, num_of_files




def clean(instr):
    return instr.translate(None, string.punctuation + '')


def parse_RSS_feed(url):
	pass

def getVideoMetadata(filename):
	full_path = MEDIA_ROOT + filename
	result = subprocess.Popen(["ffprobe", full_path], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	return result.stdout.readlines()


def getDurationMetadata(filename):
	full_path = MEDIA_ROOT + filename
	result = subprocess.Popen(["ffprobe", full_path], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	return [x for x in result.stdout.readlines() if "Duration" in x]

def getMediaInfoMetadata(filename):
	full_path = MEDIA_ROOT + filename
	result = subprocess.Popen(["mediainfo", full_path], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	return result.stdout.readlines()