from rest_framework import serializers
from models import *


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

    # # remove hypen from UUID
    # def to_representation(self, instance):
    #     ret = super(LocationSerializer, self).to_representation(instance)
    #     ret['location_id'] = ret['location_id'].replace('-', '')
    #     return ret
