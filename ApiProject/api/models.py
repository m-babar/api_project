import uuid

from django.db import models
from django.contrib.auth.models import User


class AbstractBaseModel(models.Model):
    """
    It's abstract base model to reduce code reputation.
    """
    Title = models.CharField(max_length=52, verbose_name="Title")
    Uid = models.UUIDField(unique=True, default=uuid.uuid4, blank=True)

    created_by = models.ForeignKey(User, verbose_name='Created by', related_name="create_%(class)s")

    class Meta:
        abstract = True


class Playlist(AbstractBaseModel):
    """
    It's playlist model to store the all information of the playlist.
    """

    PROCESSING = 'PROCESSING'
    ENCODING = 'ENCODING '
    COMPLETED = 'COMPLETED' 
    SCHEDULED = 'SCHEDULED'
    PLAYING = 'PLAYING'


    STATUS_CHOICES = (
       (PROCESSING, PROCESSING),
       (ENCODING, ENCODING),
       (COMPLETED, COMPLETED),
       (SCHEDULED, SCHEDULED),
       (PLAYING, PLAYING),
    )

    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PROCESSING, verbose_name='Status' )

    CreatedOn = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    CompletedOn = models.DateTimeField(auto_now_add=True, verbose_name='Completed on')
    Uri = models.URLField(max_length=512, verbose_name='URL')
    ProcessedOn = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    ScheduledOn = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    Duration = models.TimeField(verbose_name="Duration", auto_now_add=True)
    

    def __str__(self):
       return '%s'%(self.Uid) 


    @property
    def playlist_assests_count(self):
        # it's return number of assest counts to associated with each playlist
        return self.assests.count()


class Assest(AbstractBaseModel):
    """
    Assest model to sotre the information of video content. it's associated with 
    playlist model.
    """

    MOVIE = 'MOVIE'
    TVSHOW = 'TVSHOW'
    ADVERTISEMENT = 'ADVERTISEMENT' 
    BUMPER = 'BUMPER'
    PROMO = 'PROMO' 


    STATUS_CHOICES = (
       (MOVIE, MOVIE),
       (TVSHOW, TVSHOW),
       (ADVERTISEMENT, ADVERTISEMENT),
       (BUMPER, BUMPER),
       (PROMO, PROMO),
    )

    Uri = models.URLField(max_length=512, verbose_name='URI')
    Type = models.CharField(max_length=10, choices=STATUS_CHOICES, default=TVSHOW, verbose_name='Type' )
    
    playlist = models.ForeignKey(Playlist, related_name='assests')


    def __str__(self):
        return self.Title


class Schedule(AbstractBaseModel):
    """
    It's store the information to schedule the playlist.
    """

    StartAt = models.DateTimeField(verbose_name='StartAt')
    isLoop = models.BooleanField(verbose_name='is loop')

    playlist = models.ForeignKey(Playlist, related_name="schedules")


    def __str__(self):
        return self.Title