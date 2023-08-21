from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Driver)
admin.site.register(Client)
admin.site.register(Trip)
admin.site.register(Docket)
admin.site.register(AdminTruck)
admin.site.register(ClientTruckConnection)


