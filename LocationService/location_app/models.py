from __future__ import unicode_literals
from django.db import models
import uuid


# Create your models here.
class Location(models.Model):
    class Meta:
        db_table = 'location'

    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    aptNumber = models.CharField(max_length=200)
    streetAddress = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipCode = models.IntegerField()
    active = models.BooleanField()
