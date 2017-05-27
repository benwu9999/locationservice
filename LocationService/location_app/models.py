from __future__ import unicode_literals
from django.db import models
import uuid


# Create your models here.
class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    aptNumber = models.CharField(max_length=200)
    streetAddress = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipCode = models.IntegerField()
    active = models.BooleanField()


class CommuteInfo(models.Model):
    commute_info_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seeker_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='seeker_location',
        null=True,
        blank=True
    )
    job_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='job_location',
        null=True,
        blank=True
    )
    distance = models.IntegerField()  # number of miles
    transit_time = models.ForeignKey(
        CommuteTime,
        on_delete=models.SET_NULL,
        related_name='transit_time',
        null=True,
        blank=True
    )
    drive_time = models.ForeignKey(
        CommuteTime,
        on_delete=models.SET_NULL,
        related_name='drive_time',
        null=True,
        blank=True
    )


class CommuteTime(models.Model):
    commute_time_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hour = models.IntegerField()
    minute = models.IntegerField()
