import json

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import *


# Create your views here.
class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'location_id'
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationById(APIView):
    def get(self, request, format=None):
        locations = Location.objects.filter(location_id__in=request.data['ids'].split(','))
        return Response(locations)
