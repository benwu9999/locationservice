from rest_framework import serializers

from models import CommuteInfo


class CommuteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteInfo
        fields = '__all__'
