import datetime
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from models import CommuteInfo, CommuteTime

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
        dicts = request.data

        now = datetime.datetime.now()
        commute_infos = []
        for dict in dicts:
            drive_time_dict = dict.pop('drive_time')
            drive_time, created = CommuteTime.objects.get_or_create(**drive_time_dict)
            # if created:
            #     drive_time_dict['created'] = now
            dict['drive_time'] = drive_time

            transit_time_dict = dict.pop('transit_time')
            transit_time, created = CommuteTime.objects.get_or_create(**transit_time_dict)
            # if created:
            #     transit_time_dict['created'] = now
            dict['transit_time'] = transit_time

            dict['seeker_location_id'] = dict.pop('seeker_location')['location_id']
            dict['job_location_id'] = dict.pop('job_location')['location_id']

            commute_info = CommuteInfo(**dict)
            commute_info.created = now
            commute_infos.append(commute_info)

        CommuteInfo.objects.bulk_create(commute_infos)
        return Response(len(commute_infos), status=status.HTTP_201_CREATED)


class CommuteInfoBulkGet(APIView):
    def post(self, request, format=None):
        data = request.data
        seeker_location_id = data['seeker_location']['location_id']
        job_location_ids = data['job_location_ids']
        commute_infos = CommuteInfo.objects.filter(seeker_location_id=seeker_location_id,
                                              job_location_id__in=job_location_ids)
        z = CommuteInfoSerializer(commute_infos, many=True)
        return Response(z.data)
