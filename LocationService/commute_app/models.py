from __future__ import unicode_literals

import uuid

from django.db import models
from django_unixdatetimefield import UnixDateTimeField


class CommuteTime(models.Model):
    class Meta:
        db_table = 'commute_time'

    commute_time_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hour = models.IntegerField()
    minute = models.IntegerField()
    created = UnixDateTimeField(null=True, blank=True)


class CommuteInfo(models.Model):
    class Meta:
        db_table = 'commute_info'

    commute_info_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seeker_location_id = models.CharField(max_length=200, null=True)
    job_location_id = models.CharField(max_length=200, null=True)
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
    created = UnixDateTimeField(null=True, blank=True)
    modified = UnixDateTimeField(auto_now=True)
