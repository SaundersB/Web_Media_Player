from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone

# Models
class AudioTrack(models.Model):
	song_title = models.CharField(max_length=50, null=True)
	artist = models.CharField(max_length=100, null=True)
	performer = models.CharField(max_length=100, null=True)
	album = models.CharField(max_length=100, null=True)
	date_added = models.DateField(max_length=20, null=True)
	genre = models.CharField(max_length=50, null=True)
	play_count = models.CharField(max_length=20, null=True)
	rating = models.CharField(max_length=10, null=True)
	year = models.CharField(max_length=20,null=True)
	track_number = models.CharField(max_length=200, null=True)
	track_title = models.CharField(max_length=200, null=True)
	file_size = models.CharField(max_length=20, null=True)
	file_name = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(default=timezone.now,blank=True)

	#def __str__(self):
	#	return u'%s %s %s %s %s %s %s %s %s %s' % (self.song_title, self.artist, self.album, self.date_added, self.genre, self.play_count, self.rating, self.year, self.track_number, self.file_size)


class VideoTrack(models.Model):
	video_title = models.CharField(max_length=50, null=True)
	video_length = models.CharField(max_length=50, null=True)
	video_width = models.CharField(max_length=50, null=True)
	video_height = models.CharField(max_length=50, null=True)
	video_aspect_ratio = models.CharField(max_length=50, null=True)
	video_frame_rate = models.CharField(max_length=50, null=True)
	video_format = models.CharField(max_length=50, null=True)
	bit_rate = models.CharField(max_length=50, null=True)
	date_added = models.DateTimeField(default=datetime.now,blank=True)
	play_count = models.IntegerField(null=True)
	rating = models.CharField(max_length=10, null=True)
	year = models.CharField(max_length=20, null=True)
	file_size = models.CharField(max_length=20, null=True)
	file_name = models.CharField(max_length=20, null=True)

