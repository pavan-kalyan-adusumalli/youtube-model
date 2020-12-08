from django.db import models
from datetime import date
from sortedm2m.fields import SortedManyToManyField
d = date.today()
categories = (
    ('Not mentioned','----choose category----'),
    ('films and animation', 'Film and animation'),
    ('cars and vehicles', 'Cars and Vehicles'),
    ('music', 'Music'),
    ('pets and animals', 'Pets and animals'),
    ('sports','Sports'),
    ('travel and events', 'Travel and events'),
    ('gaming','Gaming'),
    ('people and blogs', 'People and blogs'),
    ('comedy', 'Comedy'),
    ('entertainment', 'Entertainment'),
    ('news and politics', 'News and politics'), 
    ('how-to and style', 'How-to and style'),
    ('education', 'Education'),
    ('science and technology', 'Science and Technology'),
    ('non-profit and activism', 'Non-profit and activism')
)
# Create your models here.
class ytusers(models.Model):
    username = models.CharField(max_length=80)
    userpicture = models.CharField(max_length=1000, default='')

    def __str__(self):
        return(f"{self.id} {self.username}")

class Channel(models.Model):
    owner = models.ForeignKey(ytusers, on_delete=models.CASCADE, related_name="userchannels")
    channelname = models.CharField(max_length=30)
    channelpicture = models.ImageField(upload_to='channelimages/' ,default='../static/black.png')
    coverpic = models.ImageField(default='../static/default.jpg', blank=True)
    description = models.CharField(max_length=1000 ,default='')
    date_created = models.CharField(max_length=15, default=d)
    subs = models.ManyToManyField(ytusers, blank=True, related_name="subscriptions")
    portfolio = models.CharField(max_length=500, default='', blank=True)
    fblink = models.CharField(max_length=500, default='', blank=True)
    twitterlink = models.CharField(max_length=500, default='', blank=True)
    instalink = models.CharField(max_length=500, default='', blank=True)
    

    def __str__(self):
        return(f"{self.id} {self.channelname} {self.owner} {self.date_created}")

class Video(models.Model):
    videoname = models.CharField(max_length=100)
    recording = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    subtitles = models.FileField(upload_to='subtitles/', blank=True, default='')
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=35, choices=categories)
    uploadedchannel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos")
    published_date = models.CharField(max_length=15, default=d)  
    views = models.IntegerField(default=0)
    watchHistory = SortedManyToManyField(ytusers, blank=True, related_name="watchedVideos")
    hideComments = models.BooleanField(default=False)
    like = models.ManyToManyField(ytusers, blank=True, related_name='likedvideos')
    dislikes = models.ManyToManyField(ytusers, blank=True, related_name='dislikedvideos')

class Comment(models.Model):
    content = models.CharField(max_length=500)
    owner = models.ForeignKey(ytusers, on_delete=models.CASCADE, related_name='commentator')
    videoname = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comment')
    date = models.CharField(max_length=15, default=d)

class Playlist(models.Model):
    playlistname = models.CharField(max_length=30)
    private = models.BooleanField(default=True)
    owner = models.ForeignKey(ytusers, on_delete=models.CASCADE, related_name='playlists')
    channelname = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='channelplaylists', blank=True, null=True)
    videoname = SortedManyToManyField(Video, blank=True, related_name='playlistvideos')

class WatchLater(models.Model):
    playlistname = 'watch later'
    owner = models.ForeignKey(ytusers, on_delete=models.CASCADE, related_name='watchlater')
    videos = SortedManyToManyField(Video, blank=True, related_name='watchlatervideos')
