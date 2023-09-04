from django.contrib import admin
from .models import *

# Register your models here.



class Trip_(admin.ModelAdmin):

    list_display = ['verified',"driverId", "clientName", 'truckNo',"shiftType", "startTime", 'endTime',"numberOfLog", "logSheet","source","shiftDate"]
    # search_fields = ["driverId", 'clientName']
    list_filter = ('shiftType', 'clientName')

admin.site.register(Trip,Trip_)

class Docket_(admin.ModelAdmin):

    list_display = ["docketId","tripId", 'docketNumber', 'docketFile']
    search_fields = ["docketNumber"]

admin.site.register(Docket, Docket_)

class Client_(admin.ModelAdmin):

    list_display = ["clientId","name",'docketGiven']
    search_fields = ["clientId","name"]

admin.site.register(Client, Client_)

class Source_(admin.ModelAdmin):

    list_display = ["sourceName"]
    search_fields = ["sourceName"]

admin.site.register(Source, Source_)

class AdminTruck_(admin.ModelAdmin):

    list_display = ["adminTruckNumber"]
    search_fields = ["adminTruckNumber"]

admin.site.register(AdminTruck, AdminTruck_)


class ClientTruckConnection_(admin.ModelAdmin):

    list_display = ["truckNumber", "clientId", 'clientTruckId']
    search_fields = ['clientTruckId']

admin.site.register(ClientTruckConnection, ClientTruckConnection_)

class Driver_(admin.ModelAdmin):

    list_display = ["driverId", "name", 'phone']
    search_fields = ["driverId"]

admin.site.register(Driver, Driver_)
