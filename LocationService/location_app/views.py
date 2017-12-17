import operator
import sys
import time

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers import *


class Util(object):

    @staticmethod
    def create_qs(param):
        text_qs = list()
        text_qs.append(Q(**{'name__icontains': param}))
        text_qs.append(Q(**{'state__icontains': param}))
        text_qs.append(Q(**{'country__icontains': param}))
        text_qs.append(Q(**{'street_address__icontains': param}))
        text_qs.append(Q(**{'city__icontains': param}))
        text_qs.append(Q(**{'zip_code__icontains': param}))
        return text_qs


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def post(self, request, *args, **kwargs):

        location_dict = request.data
        if 'location_id' not in location_dict:
            okStatus = status.HTTP_201_CREATED
        else:
            okStatus = status.HTTP_200_OK
        location = Location(**location_dict)
        location.save()
        return Response(LocationSerializer(location).data, status=okStatus)


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationSearch(APIView):
    def get(self, request, format=None):
        try:
            qs = list()
            if 'ids' in request.query_params:
                qs.append(Q(pk__in=request.query_params['ids'].split(',')))
            if 'within' in request.query_params:
                qs.append(Q(created__gt=self.get_epoch(request.query_params['within'])))
            if 'has' in request.query_params:
                for param in request.query_params['has'].split(","):
                    text_qs = Util.create_qs(param)
                    qs.append(reduce(operator.or_, text_qs))
            z = LocationSerializer(Location.objects.filter(reduce(operator.or_, qs)), many=True)
            return Response(z.data)
        except:
            return Response(sys.exc_info()[0])

    def get_epoch(self, epoch):
        return int(time.time()) - epoch


class LocationByText(GenericAPIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            id_only = False
            if 'id_only' in request.data and request.data['id_only'] == True:
                id_only = True

            # profile id -> profile dict
            id_dict = dict()
            # text -> [ids...]
            text_to_id_dict = dict()
            if 'has' in request.data:
                if id_only:
                    for param in request.data['has'].split(","):
                        text_qs = Util.create_qs(param)
                        ids = Location.objects.values_list('location_id', flat=True).filter(
                            reduce(operator.or_, text_qs))
                        text_to_id_dict[param] = ids
                    return Response(text_to_id_dict)
                else:
                    for param in request.data['has'].split(","):
                        text_qs = Util.create_qs(param)
                        z = LocationSerializer(Location.objects.filter(reduce(operator.or_, text_qs)),
                                               many=True)
                        ids = list()
                        for p in z.data:
                            id = p['location_id']
                            if id not in id_dict:
                                id_dict[id] = p
                            ids.append(id)
                        text_to_id_dict[param] = ids
                    ret = dict()
                    ret['idDict'] = id_dict
                    ret['textDict'] = text_to_id_dict
                    return Response(ret)
        except:
            return Response(sys.exc_info()[0])


class LocationSearchByIds(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        if 'ids' in request.query_params:
            q = Q(pk__in=request.query_params['ids'].split(','))
            z = LocationSerializer(Location.objects.filter(q), many=True)
            return Response(z.data)
        return Response([])
