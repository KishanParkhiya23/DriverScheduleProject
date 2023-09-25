import csv 
from Invoice_analysis_app.models import *

def dateConvert(date_):
    date_ = date_.split('/')
    year_ ='20' + date_[-1]
    return year_ + '-' + date_[1] + '-' + date_[0]

def insertIntoModel(dataList):
    # dataList = data.split(',')
    DocketPDFobj = DocketPDF()
    
    DocketPDFobj.truckNo = float(dataList[0])
    DocketPDFobj.docketNumber = float(dataList[1])
    DocketPDFobj.save()
    dataList  = dataList[2:]
    
    while dataList:
        dump = dataList[:10]
        if dump[2].upper().strip() == "TRUCK TRANSFER PER KM":
            truckCostObj = transferKMSCost()
            truckCostObj.docketNo = DocketPDF.objects.filter(docketNumber = DocketPDFobj.docketNumber).first()
            truckCostObj.deliveryDate = dateConvert(dump[0])
            truckCostObj.source = dump[1]
            truckCostObj.paidKMS = float(dump[3]) if dump[3] != '' else 0
            truckCostObj.invoiceQuantity = float(dump[4])
            truckCostObj.unit = dump[5]
            truckCostObj.unitPrice = float(dump[6])
            truckCostObj.TotalExGST = float(dump[7]) if dump[7][0] != '(' else float(dump[7][1:-1])
            truckCostObj.GSTPayable = float(dump[8]) if dump[8][0] != '(' else float(dump[8][1:-1])
            truckCostObj.TotalInGST = float(dump[9]) if dump[9][0] != '(' else float(dump[9][1:-1])
            truckCostObj.save()
            
        elif dump[2].upper().strip() == "FEE SERVICE WAITING TIME PER MINUTE":
            waitingCostObj = WaitingTimeCost()
            waitingCostObj.docketNo = DocketPDF.objects.filter(docketNumber = DocketPDFobj.docketNumber).first()
            waitingCostObj.deliveryDate = dateConvert(dump[0])
            waitingCostObj.source = dump[1]
            waitingCostObj.paidKMS = float(dump[3]) if dump[3] != '' else 0
            waitingCostObj.invoiceQuantity = float(dump[4])
            waitingCostObj.unit = dump[5]
            waitingCostObj.unitPrice = float(dump[6])
            waitingCostObj.TotalExGST = float(dump[7]) if dump[7][0] != '(' else float(dump[7][1:-1])
            waitingCostObj.GSTPayable = float(dump[8]) if dump[8][0] != '(' else float(dump[8][1:-1])
            waitingCostObj.TotalInGST = float(dump[9]) if dump[9][0] != '(' else float(dump[9][1:-1])
            waitingCostObj.save()
            
        dataList = dataList[10:]
        
f = open("File_name_file.txt",'r')
file_name = f.read()

files = open(f'static/img/Invoice/{file_name}','r')
reader=csv.reader(files)
next(reader)
for row in reader:
    insertIntoModel(row)