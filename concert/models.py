from django.utils.timezone import localdate

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Concert(models.Model):
    concert_name = models.CharField(max_length=255)
    duration = models.FloatField()
    city = models.CharField(max_length=255)
    date = models.DateField(default=localdate)

    def __str__(self):
        return self.concert_name


class ConcertAttending(models.Model):
    class AttendingChoices(models.TextChoices):
        NOTHING = "-", _("-")
        NOT_ATTENDING = "Not Attending", _("Not Attending")
        ATTENDING = "Attending", _("Attending")

    concert = models.ForeignKey(
        Concert, null=True, on_delete=models.CASCADE, related_name="attendee"
    )
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    attending = models.CharField(
        max_length=100,
        choices=AttendingChoices.choices,
        default=AttendingChoices.NOTHING,
    )

    class Meta:
        unique_together = ['concert', 'user']

    def __str__(self):
        return self.attending


class Photo(models.Model):
    pic_url = models.URLField()
    event_country = models.CharField(max_length=255)
    event_state = models.CharField(max_length=255)
    event_city = models.CharField(max_length=255)
    event_date = models.CharField(max_length=30)

    class Meta:
        managed = False

    def __str__(self):
        return self.pic_url


class Song(models.Model):
    title = models.CharField(max_length=255)
    lyrics = models.TextField()

    class Meta:
        managed = False

    def __str__(self):
        return self.title
