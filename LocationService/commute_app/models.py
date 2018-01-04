from __future__ import unicode_literals

import datetime

import dateutil.parser
from django.db import models
from django_unixdatetimefield import UnixDateTimeField


class CommuteInfo(models.Model):
    """
    transit_time - in minute
    drive_time - in minute
    """
    class Meta:
        db_table = 'commute_info'

    commute_info_id = models.CharField(primary_key=True, max_length=200, null=False)
    distance = models.FloatField()  # number of miles
    transit_time = models.IntegerField(null=True)
    drive_time = models.IntegerField(null=True)
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.transit_time.save()
        self.drive_time.save()
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(CommuteInfo, self).save()
