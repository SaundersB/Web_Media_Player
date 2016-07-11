from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AudioTrack(models.Model):
	song_title = models.CharField(max_length=50)
	artist = models.CharField(max_length=100)
	album = models.CharField(max_length=100)
	date_added = models.DateField()
	genre = models.CharField(max_length=50)
	play_count = models.IntegerField()
	rating = models.CharField(max_length=10)
	year = models.IntegerField()
	track_number = models.IntegerField()
	file_size = models.DecimalField(max_digits=20, decimal_places=5)

	def __str__(self):
		return u'%s %s %s %s %s %s %s %s %s %s' % (self.song_title, self.artist, self.album, self.date_added, self.genre, self.play_count, self.rating, self.year, self.track_number, self.file_size)

