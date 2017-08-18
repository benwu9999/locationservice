import json

import sys
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


class LocationSearch(APIView):
    def get(self, request, format=None):
        try:
            if 'ids' in request.query_params:
                serializer = LocationSerializer(Location.objects.filter(
                    pk__in=request.query_params['ids'].split(',')), many=True)

                return Response(serializer.data)
        except:
            return Response(sys.exc_info()[0])
