import time
import sys

import operator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from serializers import *


# Create your views here.
class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


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
