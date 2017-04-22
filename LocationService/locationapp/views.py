from django.shortcuts import render
from django.http import HttpResponse
from locationapp.models import Location
from locationapp.serializers import LocationSerializer
from rest_framework import generics
def index(request):
        return HttpResponse("Hello world! This is our Location App.")
# Create your views here.

class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = Location.objects.all()
        serializer_class = LocationSerializer
