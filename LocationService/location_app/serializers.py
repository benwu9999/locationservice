from rest_framework import serializers
from models import *


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CommuteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteInfo
        fields = '__all__'


class CommuteTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteTime
        fields = '__all__'