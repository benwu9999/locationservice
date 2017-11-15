import time

from rest_framework import serializers

class UnixEpochDateField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))