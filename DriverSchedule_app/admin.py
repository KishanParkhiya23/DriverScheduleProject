from django.contrib import admin
from .models import *

# Register your models here.



class Trip_(admin.ModelAdmin):

    list_display = ["driverId", "clientName", 'truckNo',"shiftType", "startDateTime", 'endDateTime',"numberOfLoad", "loadSheet"]
    search_fields = ["driverId", 'clientName', 'truckNo']

admin.site.register(Trip, Trip_)

class Docket_(admin.ModelAdmin):

    list_display = ["docketId","tripId", 'docketNumber', 'docketFile']
    search_fields = ["docketId","tripId","docketNumber" ]

admin.site.register(Docket, Docket_)

class Client_(admin.ModelAdmin):

    list_display = ["clientId","name"]
    search_fields = ["clientId","name"]

admin.site.register(Client, Client_)

class AdminTruck_(admin.ModelAdmin):

    list_display = ["adminTruckNumber"]
    search_fields = ["adminTruckNumber"]

admin.site.register(AdminTruck, AdminTruck_)


class ClientTruckConnection_(admin.ModelAdmin):

    list_display = ["truckNumber", "clientId", 'clientTruckId']
    search_fields = ["truckNumber", 'clientId', 'clientTruckId']

admin.site.register(ClientTruckConnection, ClientTruckConnection_)

class Driver_(admin.ModelAdmin):

    list_display = ["driverId", "name", 'phone']
    search_fields = ["driverId", 'name', 'phone']

admin.site.register(Driver, Driver_)
