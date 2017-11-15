import time
import sys

import operator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from serializers import *


# Create your views here.
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
                text_qs = list()
                text_qs.append(Q(**{'name__icontains': request.query_params['has']}))
                text_qs.append(Q(**{'state__icontains': request.query_params['has']}))
                text_qs.append(Q(**{'country__icontains': request.query_params['has']}))
                text_qs.append(Q(**{'street_address__icontains': request.query_params['has']}))
                text_qs.append(Q(**{'city__icontains': request.query_params['has']}))
                text_qs.append(Q(**{'zip_code__icontains': request.query_params['has']}))
                qs.append(reduce(operator.or_, text_qs))
            z = LocationSerializer(Location.objects.filter(reduce(operator.and_, qs)), many=True)
            return Response(z.data)
        except:
            return Response(sys.exc_info()[0])

    def get_epoch(self, epoch):
        return int(time.time()) - epoch


class LocationSearchByIds(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        if 'ids' in request.query_params:
            q = Q(pk__in=request.query_params['ids'].split(','))
            z = LocationSerializer(Location.objects.filter(q), many=True)
            return Response(z.data)
        return Response([])
