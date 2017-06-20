from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from models import CommuteInfo

from serializers import CommuteInfoSerializer


class CommuteInfoList(generics.ListCreateAPIView):
    queryset = CommuteInfo.objects.all()
    serializer_class = CommuteInfoSerializer


class CommuteInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    lookup_field = 'commuteInfoId'
    queryset = CommuteInfo.objects.all()
    serializer_class = CommuteInfoSerializer


class CommuteInfoBulkSave(APIView):
    def post(self, request, format=None):
        data = request.POST
        commute_infos = data['commutes']
        CommuteInfo.objects.bulk_create([CommuteInfo(**json.loads(c)) for c in commute_infos])
        return Response(len(commute_infos), status=status.HTTP_201_CREATED)


class CommuteInfoBulkGet(APIView):
    def get(self, request, format=None):
        data = request.data
        seeker_location_id = data['seekerLocation'].id
        job_location_ids = data['jobLocationIds']
        commutes = CommuteInfo.objects.filter(seeker_location_id=seeker_location_id,
                                              job_location_id__in=job_location_ids)
        return Response(commutes)
