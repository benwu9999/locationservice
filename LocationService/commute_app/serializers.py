from rest_framework import serializers
from shared.utils import UnixEpochDateField
from models import CommuteInfo, CommuteTime


class CommuteTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteTime
        fields = '__all__'


class CommuteInfoSerializer(serializers.ModelSerializer):
    transit_time = CommuteTimeSerializer(many=False)
    drive_time = CommuteTimeSerializer(many=False)

    class Meta:
        model = CommuteInfo
        fields = '__all__'
