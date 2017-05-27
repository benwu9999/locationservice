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
        locations = Location.objects.filter(location_id__in = request.data['ids'].split(','))
        return Response(locations)

class CommuteInfoList(generics.ListCreateAPIView):
    queryset = CommuteInfo.objects.all()
    serializer_class = CommuteInfoSerializer

class CommuteInfoDetail(generics.RetrieveUpdateDestroyAPIView):

    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'commute_info_id'
    queryset = CommuteInfo.objects.all()
    serializer_class = CommuteInfoSerializer

class CommuteInfoBulkSave(APIView):

    def post(self, request, format=None):
        data = request.data
        commutes = data['commutes']
        CommuteInfo.objects.bulk_create([CommuteInfo(**json.loads(c)) for c in commutes])
        return Response(len(commutes))


class CommuteInfoBulkGet(APIView):

    def get(self, request, format=None):
        data = request.data
        seeker_location_id = data['seekerLocation'].id
        job_location_ids = data['jobLocationIds']
        commutes = CommuteInfo.objects.filter(seeker_location_id = seeker_location_id,
                                             job_location_id__in = job_location_ids)
        return Response(commutes)