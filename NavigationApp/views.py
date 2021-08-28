import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import datetime
from django.core.cache import cache

from NavigationApp.models import NavigationRecord, Vehicle
from NavigationApp.serializers import LastPointsSerializer, NavigationRecordSerializer, VehicleSerializer

# Create your views here.

@csrf_exempt
def vehicleApi(request, id=0):
    if request.method == "GET":
        vehicles = Vehicle.objects.all()
        vehicles_serializer = VehicleSerializer(vehicles, many=True)
        return JsonResponse(vehicles_serializer.data, safe=False)
    elif request.method == "POST":
        vehicle_data = JSONParser().parse(request)
        vehicles_serializer=VehicleSerializer(data=vehicle_data)
        if vehicles_serializer.is_valid():
            vehicles_serializer.save()
            return JsonResponse("Vehicle added.", safe=False)
        return JsonResponse("Failed to Add.", safe=False)
    elif request.method == "PUT":
        vehicle_data = JSONParser().parse(request)
        vehicle = Vehicle.objects.get(id=vehicle_data['id'])
        vehicles_serializer=VehicleSerializer(vehicle, data=vehicle_data)
        if vehicles_serializer.is_valid():
            vehicles_serializer.save()
            return JsonResponse("Updated vehicle successfuly.", safe=False)
        return JsonResponse("Failed to update vehicle.", safe=False)
    elif request.method == "DELETE":
        vehicle = Vehicle.objects.get(id=id)
        vehicle.delete()
        return JsonResponse("Deleted vehicle successfuly.", safe=False)

@csrf_exempt
def NavigationApi(request, id=0):
    if request.method == "GET":
        navRecord = NavigationRecord.objects.all()
        navRecord_serializer = NavigationRecordSerializer(navRecord, many=True)
        return JsonResponse(navRecord_serializer.data, safe=False)
    elif request.method == "POST":
        navRecord_data = JSONParser().parse(request)
        navRecord_serializer=NavigationRecordSerializer(data=navRecord_data)
        if navRecord_serializer.is_valid():
            navRecord_serializer.save()
            return JsonResponse("Navigation record added.", safe=False)
        print(navRecord_serializer._errors)
        return JsonResponse({"message":"Failed to Add.", **navRecord_serializer._errors}, safe=False)
    elif request.method == "PUT":
        navRecord_data = JSONParser().parse(request)
        navRecord = NavigationRecord.objects.get(id=navRecord_data['id'])
        navRecord_serializer=NavigationRecordSerializer(navRecord, data=navRecord_data)
        if navRecord_serializer.is_valid():
            navRecord_serializer.save()
            return JsonResponse("Updated navigation record successfuly.", safe=False)
        return JsonResponse("Failed to update navigation record.", safe=False)
    elif request.method == "DELETE":
        navRecord = NavigationRecord.objects.get(id=id)
        navRecord.delete()
        return JsonResponse("Deleted navigation record successfuly.", safe=False)


@csrf_exempt
def LastPointsApi(request, lastHours=24):
    if request.method == "GET":
        time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=int(lastHours)) + datetime.timedelta(hours=3)
        query = NavigationRecord.objects.select_related().filter(datetime__gte=time_threshold)
        lastPointsList = list(query.values('latitude', 'longitude', 'vehicle__plate', 'datetime'))
        for record in lastPointsList:
            record['vehicle_plate'] = record['vehicle__plate']
            del record['vehicle__plate']

        lastPoints_serializer = LastPointsSerializer(lastPointsList, many=True)
        return JsonResponse(lastPoints_serializer.data, safe=False)

@csrf_exempt
def CacheDates(request):
    if request.method == "GET":
        query = NavigationRecord.objects.all()
        records = list(query.values('id', 'datetime'))
        for record in records:
            date = str(record['datetime'].date())
            if date in cache:
                continue
            print(date)
            cache.set(date, record["id"], None)
        return JsonResponse("Date Indexes Are Cached.", safe=False)

@csrf_exempt
def LastPointsWithCache(request, lastHours=24):
    if request.method == "GET":
        time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=int(lastHours)) + datetime.timedelta(hours=3)
        print(str(time_threshold.date()))
        starting_index = cache.get(str(time_threshold.date()))
        if starting_index:
            query = NavigationRecord.objects.select_related().filter(id__gte=starting_index)
            lastPointsList = list(query.values('latitude', 'longitude', 'vehicle__plate', 'datetime'))
            return_records = []
            for record in lastPointsList:
                if record['datetime'] > time_threshold:
                    record['vehicle_plate'] = record['vehicle__plate']
                    del record['vehicle__plate']
                    return_records.append(record)
            
            lastPoints_serializer = LastPointsSerializer(return_records, many=True)
            return JsonResponse(lastPoints_serializer.data, safe=False)
        else:
            return JsonResponse("No records found in cache.", safe=False)
