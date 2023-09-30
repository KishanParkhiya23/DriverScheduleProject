from django.contrib import admin
from .models import *
from schedule_trip.models import *
from django.core.mail import send_mail, EmailMessage

# Register your models here.



class DocketInline(admin.StackedInline):
    model = Docket
    fieldsets=[
        (
            "docket_details",
            {
                "fields" : 
                    ["docketId","tripId","docketNumber","docketFile","waitingTime","waitingTimeCost","transferKMS","transferKMSCost","cubicMl","cubicMlCost","minLoad","minLoadCost","others","othersCost","total_cost"]
            } 
        )
    ]
        
    readonly_fields = ["total_cost"]
    extra = 0
    
class Trip_(admin.ModelAdmin):

    list_display = ['verified',"driverId", "clientName", 'truckNo',"shiftType", "startTime", 'endTime',"numberOfLoads", "logSheet","basePlant","shiftDate"]
    # search_fields = ["driverId", 'clientName']
    list_filter = ('shiftType', 'clientName')
    
    inlines = [DocketInline]

admin.site.register(Trip,Trip_)

class Docket_(admin.ModelAdmin):

    list_display = ["docketId","tripId", 'docketNumber', 'docketFile','total_cost']
    search_fields = ["docketNumber"]

admin.site.register(Docket, Docket_)

class Client_(admin.ModelAdmin):

    list_display = ["clientId","name",'docketGiven']
    search_fields = ["clientId","name"]

admin.site.register(Client, Client_)

class BasePlant_(admin.ModelAdmin):

    list_display = ["basePlant"]
    search_fields = ["basePlant"]

admin.site.register(BasePlant, BasePlant_)

class ClientTruckInline(admin.TabularInline):
    model = ClientTruckConnection
    extra = 0
  
class CostInline_(admin.TabularInline):
    model =  Cost
    extra = 0  
class AdminTruck_(admin.ModelAdmin):

    list_display = ["adminTruckNumber"]
    search_fields = ["adminTruckNumber"]

    inlines = [ClientTruckInline,CostInline_]
     
admin.site.register(AdminTruck, AdminTruck_)


# class ClientTruckConnection_(admin.ModelAdmin):

#     list_display = ["truckNumber", "clientId", 'clientTruckId']
#     search_fields = ['clientTruckId']

# admin.site.register(ClientTruckConnection, ClientTruckConnection_)

class LeaveReqAdminDriver(admin.TabularInline):
    model = LeaveRequest
    extra = 0

class Driver_(admin.ModelAdmin):
    # inlines = [LeaveReqAdminDriver]
    list_display = ["driverId", "name", 'phone']
    search_fields = ["driverId"]

    def upcoming_leave_requests(self, obj):
        now = timezone.now()
        upcoming_requests = obj.leaverequest_set.filter(start_date__gte=now).order_by('start_date')[:2]
        return ', '.join([str(request) for request in upcoming_requests])

    upcoming_leave_requests.short_description = 'Upcoming Leave Requests'

admin.site.register(Driver, Driver_)

admin.site.register(LeaveRequest)
admin.site.register(NatureOfLeave)
# admin.site.register(Cost)



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

