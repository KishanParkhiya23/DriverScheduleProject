from django.contrib import admin
from .models import *
# from schedule_trip.models import *
from django.core.mail import send_mail, EmailMessage
from Driver_leave_app.models import *
from Trips_details_app.models import *
from django.http import HttpResponse
import csv

class DocketInline(admin.StackedInline):
    model = Docket
    fieldsets=[
        (
            "docket_details",
            {
                "fields" : 
                    ["docketId","tripId","docketNumber","docketFile","waitingTimeInMinutes","waitingTimeCost","transferKMS","transferKMSCost","cubicMl","cubicMlCost","minLoad","minLoadCost","others","othersCost","total_cost"]
            } 
        )
    ]
        
    readonly_fields = ["total_cost"]
    extra = 0

def driver_trip_download_csv(modeladmin, request, queryset):
    # Create a response object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DriverTripInfo.csv"'

    # Create a CSV writer using the response object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(["verified", "driverId", "clientName", "shiftType",
                     "numberOfLoads", "truckNo", "shiftDate", "basePlant", "startTime", "endTime", "logSheet",
                     "comment", "docketId", "docketNumber", "docketFile",
                     "waitingTimeInMinutes", "waitingTimeCost", "transferKMS",
                     "transferKMSCost", "cubicMl", "cubicMlCost",
                     "minLoad", "minLoadCost", "others",
                     "othersCost"])

 # Write data rows
    for driver_trip in queryset:
        # print(queryset)
        row_data = [
            driver_trip.verified,
            driver_trip.driverId,
            driver_trip.clientName,
            driver_trip.shiftType,
            driver_trip.numberOfLoads,
            driver_trip.truckNo,
            driver_trip.shiftDate,
            driver_trip.basePlant,
            driver_trip.startTime,
            driver_trip.endTime,
            driver_trip.logSheet,
            driver_trip.comment,
            
            '', '', '', '', '', '', '', '', '', '', '', '', '' # Initialize empty placeholders for other fields
        ]
    
        for docket in driver_trip.docket_set.all():
            row_data[12:25] = [docket.docketId, docket.docketNumber,
                    docket.docketFile,docket.waitingTimeInMinutes, docket.waitingTimeCost,
                    docket.transferKMS,docket.transferKMSCost, docket.cubicMl,
                    docket.cubicMlCost,docket.minLoad, docket.minLoadCost,
                    docket.others,docket.othersCost]

        # Only write the row if at least admin truck data is present
        if driver_trip.driverId:
            writer.writerow(row_data)

    return response

class DriverTrip_(admin.ModelAdmin):

    list_display = ['verified',"driverId", "clientName", 'truckNo',"shiftType", "startTime", 'endTime',"numberOfLoads", "logSheet","basePlant","shiftDate"]
    # search_fields = ["driverId", 'clientName']
    list_filter = ('shiftType', 'clientName')
    actions = [driver_trip_download_csv]
    inlines = [DocketInline]

admin.site.register(DriverTrip,DriverTrip_)



class WaitingTimeCost_(admin.StackedInline):
    model = WaitingTimeCost
    extra = 0
    
    list_display = ["docketNo","deliveryDate","paidKMS","invoiceQuantity","unit","unitPrice","TotalExGST","GSTPayable","TotalInGST",]
    search_fields = ["docketNo","TotalInGST"]


class TransferKMSCost_(admin.StackedInline):
    model = transferKMSCost
    extra = 0

    list_display = ["docketNo","deliveryDate","paidKMS","invoiceQuantity","unit","unitPrice","TotalExGST","GSTPayable","TotalInGST",]
    search_fields = ["docketNo","TotalInGST"]


class clientTripAdmin(admin.ModelAdmin):
    inlines = [WaitingTimeCost_ ,TransferKMSCost_]
    list_display = ["docketNumber","truckNo"]
    
    search_fields = ["docketNumber","truckNo"]
     
admin.site.register(ClientTrip, clientTripAdmin)



def download_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ClientName.csv"'

    writer = csv.writer(response)

    writer.writerow(["clientId", "name", "docketGiven"])

    for s in queryset:
        writer.writerow([s.clientId, s.name, s.docketGiven])

    return response

class ClientAdmin(admin.ModelAdmin):
    list_display = ["clientId", "name", 'docketGiven']
    search_fields = ["clientId", "name"]
    actions = [download_csv]

admin.site.register(Client, ClientAdmin)


def download_csv(modeladmin, request, queryset):
    # Create a response object with CSV content type and specify the filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="BasePlant.csv"'

    # Create a CSV writer using the response object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(["BasePlant"])

    # Write data rows
    for s in queryset:
        writer.writerow([s.basePlant])

    return response

class BasePlantAdmin(admin.ModelAdmin):
    list_display = ["basePlant"]
    search_fields = ["basePlant"]
    actions = [download_csv]

admin.site.register(BasePlant, BasePlantAdmin)

class ClientTruckInline(admin.TabularInline):
    model = ClientTruckConnection
    extra = 0
  
class CostInline_(admin.TabularInline):
    model =  Cost
    extra = 0  
    
    
# def admin_truck_download_csv(modeladmin, request, queryset):
#     # Create a response object with CSV content type
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="AdminTruckInfo.csv"'

#     # Create a CSV writer using the response object
#     writer = csv.writer(response)

#     # Write the header row
#     writer.writerow(["adminTruckNumber", "clientId", "driverId", "clientTruckId",
#                      "startDate", "endDate", "is_Active", "cost_id", "basePlant", "startDate", "endDate",
#                      "transferKMSCost", "waitingTimeCost", "cartagePerCumCost", "surchargeCost"])

#     # Write data rows
#     for admin_truck in queryset:
#         for client_truck in admin_truck.clienttruckconnection_set.all():
#             for cost in admin_truck.cost_set.all():
            
#                 writer.writerow([
#                     admin_truck.adminTruckNumber, client_truck.clientId, client_truck.driverId,
#                     client_truck.clientTruckId, client_truck.startDate, client_truck.endDate,
#                     cost.is_Active, cost.cost_id, cost.basePlant, cost.startDate, cost.endDate,
#                     cost.transferKMSCost, cost.waitingTimeCost, cost.cartagePerCumCost, cost.surchargeCost
#                 ])

#     return response


def admin_truck_download_csv(modeladmin, request, queryset):
    # Create a response object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AdminTruckInfo.csv"'

    # Create a CSV writer using the response object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(["adminTruckNumber", "clientId", "driverId", "clientTruckId",
                     "startDate", "endDate", "is_Active", "cost_id", "basePlant",
                     "startDate", "endDate", "transferKMSCost", "waitingTimeCost",
                     "cartagePerCumCost", "surchargeCost"])

    # Write data rows
    for admin_truck in queryset:
        row_data = [
            admin_truck.adminTruckNumber,
            '', '', '', '', '', '', '', '', '', '', '', '', '', '',  # Initialize empty placeholders for other fields
        ]

        for client_truck in admin_truck.clienttruckconnection_set.all():
            row_data[1:6] = [client_truck.clientId, client_truck.driverId, client_truck.clientTruckId,
                             client_truck.startDate, client_truck.endDate]

        for cost in admin_truck.cost_set.all():
            row_data[6:16] = [cost.is_Active, cost.cost_id, cost.basePlant, cost.startDate, cost.endDate,
                              cost.transferKMSCost, cost.waitingTimeCost, cost.cartagePerCumCost, cost.surchargeCost]

        # Only write the row if at least admin truck data is present
        if admin_truck.adminTruckNumber:
            writer.writerow(row_data)

    return response


class AdminTruckAdmin(admin.ModelAdmin):
    list_display = ["adminTruckNumber"]
    search_fields = ["adminTruckNumber"]
    actions = [admin_truck_download_csv]

    inlines = [ClientTruckInline, CostInline_]

admin.site.register(AdminTruck, AdminTruckAdmin)



def driver_download_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DriverRegInfo.csv"'

    writer = csv.writer(response)

    writer.writerow(["driverId", "name", "phone" , "email" , "password"])

    for s in queryset:
        writer.writerow([s.driverId, s.name, s.phone, s.email , s.password])

    return response

class Driver_(admin.ModelAdmin):
    # inlines = [LeaveReqAdminDriver]
    list_display = ["driverId", "name", 'phone']
    search_fields = ["driverId"]
    actions = [driver_download_csv]

    def upcoming_leave_requests(self, obj):
        now = timezone.now()
        upcoming_requests = obj.leaverequest_set.filter(start_date__gte=now).order_by('start_date')[:2]
        return ', '.join([str(request) for request in upcoming_requests])

    upcoming_leave_requests.short_description = 'Upcoming Leave Requests'

admin.site.register(Driver, Driver_)

# admin.site.register(LeaveRequest)

def leave_download_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DriverLeave.csv"'

    writer = csv.writer(response)

    writer.writerow(["employee", "start_date", "end_date" , "reason" , "status"])

    for s in queryset:
        writer.writerow([s.employee, s.start_date, s.end_date, s.reason , s.status])

    return response


class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ["employee","start_date","end_date","reason","status"]
    search_fields = ["employee"]
    actions = [leave_download_csv]

admin.site.register(LeaveRequest, LeaveRequestAdmin)


def nature_leave_download_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="NatureLeave.csv"'

    writer = csv.writer(response)

    writer.writerow(["reason"])

    for s in queryset:
        writer.writerow([s.reason])

    return response

class NatureOfLeaveAdmin(admin.ModelAdmin):
    list_display = ["reason"]
    search_fields = ["reason"]
    actions = [nature_leave_download_csv]

admin.site.register(NatureOfLeave, NatureOfLeaveAdmin)



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ('driver', 'client',)
    list_display = ["Title", "Start_Date_Time", "End_Date_Time", "Status", "driver"]
    list_filter = ["Status"]
    actions = ['send_email_action']

    def send_email_action(self, request, queryset):
        subject = 'Your job application status'
        message = 'Your job application status has been updated.'
        from_email = 'siddhantethansrec@example.com'  # Set your email address
        recipient_list = [applicant.driver.email for applicant in queryset]
        print(recipient_list)
        
        # Send emails to selected applicants
        for applicant in queryset:
            send_mail(subject, message, from_email, [applicant.driver.email])
            # send_notification_email(applicant.progress_set.latest('date_updated'))
        
        self.message_user(request, f'Emails sent to {len(queryset)} applicants.')
    
    send_email_action.short_description = 'Send email to selected applicants'

