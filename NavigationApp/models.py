from django.db import models
from datetime import datetime

# Create your models here.
class Vehicle(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    plate = models.CharField(max_length=50)

class NavigationRecord(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

class LastPoints(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    vehicle_plate = models.CharField(max_length=50)
    datetime = models.DateTimeField()