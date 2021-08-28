from rest_framework import serializers
from NavigationApp.models import LastPoints, Vehicle, NavigationRecord

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "plate")

class NavigationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationRecord
        fields = ("id", "vehicle", "datetime", "latitude", "longitude")

class LastPointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LastPoints
        fields = ("latitude", "longitude", "vehicle_plate", "datetime")