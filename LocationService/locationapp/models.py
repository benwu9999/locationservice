from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField
from localflavor.us.models import USZipCodeField
import uuid
# Create your models here.
class Location(models.Model):
        """
        data model for Location
        """
        COUNTRY_CHOICES = (('US', 'UNITED STATES'),)

        locationId=models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
        name=models.CharField(_('location name'), max_length=200)
        state=USStateField(_('state'), choices=STATE_CHOICES)
        country=models.CharField(_('country'), choices=COUNTRY_CHOICES, max_length=2)
        aptNumber=models.CharField(max_length=45, null=True, blank=True)
        streetAddress=models.CharField(max_length=45)
        zipCode=USZipCodeField(_('zip code'))
        active=models.BooleanField(_('active'), default=True)

        class Meta:
            verbose_name = _('location')
            verbose_name_plural = _('locations')

