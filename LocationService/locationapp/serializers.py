from rest_framework import serializers
from locationapp.models import Location
class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer to convert Location object data to primitive Python datatypes
    """

    class Meta:
        model=Location
        fields=('locationId','name','state','country','aptNumber','streetAddress','zipCode','active')
        

