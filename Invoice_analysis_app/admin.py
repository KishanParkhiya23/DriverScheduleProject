from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(WaitingTimeCost)
# admin.site.register(transferKMSCost)


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


class docketAdmin(admin.ModelAdmin):
    inlines = [WaitingTimeCost_ ,TransferKMSCost_]
    list_display = ["docketNumber","truckNo"]
    
    search_fields = ["docketNumber","truckNo"]
     
admin.site.register(DocketPDF, docketAdmin)