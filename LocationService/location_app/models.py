from __future__ import unicode_literals

# Create your models here.
import datetime
import uuid

import dateutil.parser
from django.db import models
from django_unixdatetimefield import UnixDateTimeField


class Location(models.Model):
    class Meta:
        db_table = 'location'

    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    apt_number = models.CharField(max_length=200, null=True, blank=True)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip_code = models.IntegerField()
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(Location, self).save()
