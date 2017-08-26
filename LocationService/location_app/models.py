from __future__ import unicode_literals
from django.db import models
import uuid


# Create your models here.
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
    created = UnixDateTimeField(null=True, blank=True)
    modified = UnixDateTimeField(auto_now=True)
