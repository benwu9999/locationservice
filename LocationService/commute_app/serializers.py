from rest_framework import serializers

from models import CommuteInfo, CommuteTime


class CommuteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteInfo
        fields = '__all__'


class CommuteTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteTime
        fields = '__all__'
