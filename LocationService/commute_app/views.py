import datetime
import sys

import math
from location_service_api import commute_service_utils
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from location_app.models import Location
from models import CommuteInfo
from serializers import CommuteInfoSerializer


def remove_dash(data):
    new_d = dict()
    for k in data.keys():
        l = data[k]
        if '-' in k:
            k = k.replace('-', '')
        new_d[k] = [x.replace('-', '') if '-' in x else x for x in l]
    return new_d

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
        for d in dicts:
            drive_time = d.pop('drive_time')
            # if created:
            #     drive_time_dict['created'] = now
            d['drive_time'] = drive_time

            transit_time = d.pop('transit_time')
            # if created:
            #     transit_time_dict['created'] = now
            d['transit_time'] = transit_time

            seeker_location_id = d.pop('seeker_location')['location_id'].replace('-', '')
            job_location_id = d.pop('job_location')['location_id'].replace('-', '')
            commute_info_id = commute_service_utils.get_commute_info_id(seeker_location_id, job_location_id)
            d['commute_info_id'] = commute_info_id

            commute_info = CommuteInfo(**d)
            commute_info.created = now
            commute_infos.append(commute_info)

        CommuteInfo.objects.bulk_create(commute_infos)
        return Response(len(commute_infos), status=status.HTTP_201_CREATED)


class CommuteInfoBulkGet(APIView):
    def post(self, request, format=None):
        data = request.data
        seeker_location_id = data['seeker_location']['location_id'].replace('-', '')
        job_location_ids = [x.replace('-', '') for x in data['job_location_ids']]
        commute_ids = list()
        for job_location_id in job_location_ids:
            commute_id = commute_service_utils.get_commute_info_id(seeker_location_id, job_location_id)
            commute_ids.append(commute_id)
        commute_infos = CommuteInfo.objects.filter(pk__in=commute_ids)
        z = CommuteInfoSerializer(commute_infos, many=True)
        id_to_commute_dict = dict()
        for c in z.data:
            id_to_commute_dict[c['commute_info_id']] = c
        return Response(id_to_commute_dict)


GOOGLE_API_KEY = 'AIzaSyA-5_FBn-VYB_I9oz39aOcMIpqfZU__o9I'


class CommuteInfoBulkGetPair(GenericAPIView):
    permission_classes = ()
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            id_to_commute_dict = dict()
            if data:
                data = remove_dash(data)
                commute_ids = list()
                for k, destinations in data.iteritems():
                    for dest in destinations:
                        commute_id = commute_service_utils.get_commute_info_id(k, dest)
                        commute_ids.append(commute_id)
                commutes = CommuteInfo.objects.filter(pk__in=commute_ids)
                for commute in commutes:
                    id_to_commute_dict[commute.commute_info_id] = commute
                if len(id_to_commute_dict) != len(commute_ids):
                    missing_routes = dict()
                    for k, destinations in data.iteritems():
                        for dest in destinations:
                            commute_id = commute_service_utils.get_commute_info_id(k, dest)
                            if commute_id not in id_to_commute_dict:
                                if k not in missing_routes:
                                    missing_routes[k] = list()
                                missing_routes[k].append(dest)
                    self._query_google(missing_routes, id_to_commute_dict)
            z = CommuteInfoSerializer(id_to_commute_dict.values(), many=True)
            for c in z.data:
                id_to_commute_dict[c['commute_info_id']] = c
            return Response(id_to_commute_dict)
        except:
            return Response(sys.exc_info()[0])

    @staticmethod
    def _query_google(unfound_routes, id_to_commute_dict):
        location_id_to_location_dict = dict()
        all_location_ids = list()
        for k, destinations in unfound_routes.iteritems():
            all_location_ids.append(k)
            all_location_ids.extend(destinations)

        locations = Location.objects.filter(pk__in=all_location_ids)
        for location in locations:
            location_id_to_location_dict[location.location_id.hex] = location

        import googlemaps
        gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

        for origin_id, destinations in unfound_routes.iteritems():
            origin_address = [location_id_to_location_dict[origin_id].to_address()]
            destination_addresses = [location_id_to_location_dict[x].to_address() for x in destinations]
            distance_matrix = gmaps.distance_matrix(origin_address, destination_addresses, 'driving', units='imperial')
            # (matrix of distances.Results are returned in rows, each row containing one origin paired with each destination.)
            if distance_matrix['status'] == 'OK':
                idx = 0
                for d in distance_matrix['rows']:
                    for inner_d in d['elements']:
                        if inner_d['status'] == 'OK':
                            distance = inner_d['distance']['text'].split(' ')[0]
                            commute_time = CommuteInfoBulkGetPair._get_commute_time(inner_d['duration']['value'])
                            commute_id = commute_service_utils.get_commute_info_id(origin_id, destinations[idx])
                            id_to_commute_dict[commute_id] = CommuteInfo(commute_info_id=commute_id, distance=distance,
                                                                         drive_time=commute_time);

                    idx += 1
            distance_matrix = gmaps.distance_matrix(origin_address, destination_addresses, 'transit', units='imperial')
            if distance_matrix['status'] == 'OK':
                idx = 0
                for d in distance_matrix['rows']:
                    for inner_d in d['elements']:
                        if inner_d['status'] == 'OK':
                            commute_time = CommuteInfoBulkGetPair._get_commute_time(inner_d['duration']['value'])
                            commute_id = commute_service_utils.get_commute_info_id(origin_id, destinations[idx])
                            id_to_commute_dict[commute_id].transit_time = commute_time
                            id_to_commute_dict[commute_id].save()
                    idx += 1


    @staticmethod
    def _get_commute_time(seconds):
        hour = math.floor(seconds / 60)
