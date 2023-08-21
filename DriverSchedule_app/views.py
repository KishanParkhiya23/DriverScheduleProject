from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from .models import *
from rest_framework.decorators import api_view
import requests
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import tabula
from django.contrib import messages
import shutil
import os


# To call home page 
@api_view(['GET'])
def index(request):
    if request.user.is_authenticated:
        return Response({'status': '200', 'message': 'Data Get Successfully', 'form1_data':request.session.get('_auth_user_id')})
    else:
        return render(request,'index.html')

# TO get all data from driver schedule API
@api_view(['POST'])
@csrf_protect
def getDriverData(request):
    data = {
        'driverschedule' : request.POST.get('driverschedule'),
        'startDate' : request.POST.get('startDate'),
        'endDate' : request.POST.get('endDate'),
        }   
    
    data['startDate']= (datetime.strptime( data['startDate'], "%Y-%m-%d")).strftime("%m-%d-%Y") 
    data['endDate']= (datetime.strptime( data['endDate'], "%Y-%m-%d")).strftime("%m-%d-%Y") 
    
    if data['driverschedule'] == 'availability':
        url = "https://www.driverschedule.com/api/schedule"
    elif data['driverschedule'] == 'appointments':
        url = "https://www.driverschedule.com/api/appointments"
    else:
        url = "https://www.driverschedule.com/api/shiftschedulecapacity"
        
    format_type = "json"
    access_token = "35d0a6c7-db72-4f31-a7f1-f8fbdcef5f00"  # Replace with your actual access token

    data = {
        "accesstoken": access_token,
        "startdate": data['startDate'],
        "enddate":  data['endDate'],
        "format": format_type
    }

    response = requests.post(url, data=data)
    api_data = response.json()
    return Response({'status': '200', 'message': 'Data Get Successfully', 'data': api_data})
 
 
@api_view(['GET'])
def getForm1(request):
    client_names = Client.objects.values_list('name', flat=True).distinct()
    driver_ids = Driver.objects.values_list('driverId', flat=True).distinct()
    admin_truck_no = AdminTruck.objects.values_list('adminTruckNumber', flat=True).distinct()
    client_truck_no = ClientTruckConnection.objects.values_list('clientTruckId', flat=True).distinct()
    
    return render(request, 'DriverSchedule_app/form1.html', {'driver_ids': driver_ids ,'client_ids' : client_names,'admin_truck_no' : admin_truck_no,'client_truck_no' : client_truck_no} )


@api_view(['GET'])
def getForm2(request):
    if 'data' in request.session:
        params = {        
            'loads' :[i+1 for i in range(int( request.session['data'].get('numberOfLoads')))]
        } 
        return render(request,'DriverSchedule_app/form2.html',params)
    else:
        return redirect('DriverSchedule_app:form1')


@csrf_protect
@api_view(['POST'])
def createFormSession(request):
    loadSheet = request.FILES.get('loadSheet')


    if loadSheet:
       
        load_sheet_folder_path = 'Temp_Load_Sheet'
        fileName = loadSheet.name
        time = (str(timezone.now())).replace(':','').replace('-','').replace(' ','').split('.')
        time = time[0]
        load_sheet_new_filename = time + '!_@' + fileName.replace(" ", "").replace("\t", "") 
        lfs = FileSystemStorage(location=load_sheet_folder_path)
        l_filename = lfs.save(load_sheet_new_filename, loadSheet)
        
        request.session['data']={
            'driverId':request.POST.get('driverId'),
            'clientName':request.POST.get('clientName'),
            'truckNum':request.POST.get('truckNum'),
            'startDateTime':request.POST.get('startDateTime'),
            'endDateTime':request.POST.get('endDateTime'),
            'loadSheet':load_sheet_new_filename,
            'shiftType':request.POST.get('shiftType'),
            'numberOfLoads':request.POST.get('numberOfLoads'),
            'comments':request.POST.get('comments')
        }
        

    request.session.set_expiry(60 *5)
    return redirect ('DriverSchedule_app:form2')
        

        
@csrf_protect
@api_view(['POST'])
def formsSave(request):
    
    driverId = request.session['data']['driverId']   
    clientName = request.session['data']['clientName'] 
    shiftType = request.session['data']['shiftType']
    numberOfLoad = request.session['data']['numberOfLoads']
    truckNo = request.session['data']['truckNum']             
    startDateTime = request.session['data']['startDateTime']    
    endDateTime = request.session['data']['endDateTime']    
    loadSheet = request.session['data']['loadSheet']    
    comment = request.session['data']['comments']    
    
    
    
  
    shutil.move('Temp_Load_Sheet/' + loadSheet, 'Final_Load_Sheet/') if not os.path.exists('Final_Load_Sheet/' + loadSheet) else None

    
    driver = Driver.objects.get(driverId=driverId)

    trip = Trip(
        driverId=driver,
        clientName=clientName,
        shiftType=shiftType,
        numberOfLoad=numberOfLoad,
        truckNo=truckNo,
        startDateTime=startDateTime,
        endDateTime=endDateTime,
        loadSheet=loadSheet,  # Use the filename or None
        comment=comment
    )
    trip.save()
    
    Docket_no = []
    Docket_file = []

    for i in range(1,int(numberOfLoad)+1):
        key = f"docketNumber[{i}]"
        docket_number = request.POST.get(key)
        Docket_no.append(docket_number)
        key_files = f"docketFile[{i}]"
        docket_files = request.FILES.get(key_files)
        print(docket_files)

        if docket_files:
            # Specify the folder path where you want to save the file
            
            # PDF ---------------
            pdf_folder_path = 'Docket_File'
            fileName = docket_files.name
            time = (str(timezone.now())).replace(':','').replace('-','').replace(' ','').split('.')
            time = time[0]
            docket_new_filename = time + '!_@' + fileName.replace(" ", "").replace("\t", "") 
            pfs = FileSystemStorage(location=pdf_folder_path)
            p_filename = pfs.save(docket_new_filename, docket_files)
            Docket_file.append(docket_new_filename)
            
            
    for i in range(len(Docket_no)):
        docket_ = Docket(
            tripId=trip,
            docketNumber=Docket_no[i],  # Use the specific value from the list
            docketFile=Docket_file[i],  # Use the specific value from the list
        )
        docket_.save()
    
    
    del request.session['data']
    
    messages.success(request, " Form Successfully Filled Up")
    return redirect('/')


def getFileForm(request):
    return render(request,'DriverSchedule_app/fileForm.html')

@csrf_protect
@api_view(['POST'])
def saveFileForm(request):
    pdf_file = request.FILES.get('pdf_file')

    if pdf_file:
        # Specify the folder path where you want to save the file
        
        # PDF ---------------
        pdf_folder_path = 'PDF'
        fileName = pdf_file.name
        time = (str(timezone.now())).replace(':','').replace('-','').replace(' ','').split('.')
        time = time[0]
        pdf_new_filename = time + '!_@' + fileName.replace(" ", "").replace("\t", "") 
        pfs = FileSystemStorage(location=pdf_folder_path)
        p_filename = pfs.save(pdf_new_filename, pdf_file)

        csv_name = pdf_new_filename.replace('.pdf','.csv')
        
        # CSV--------------- 
        tabula.convert_into('PDF/'+pdf_new_filename, "CSV/"+csv_name, output_format="csv", pages='all')
 

        return Response({'status': '200', 'message': 'Data Get Successfully','file':p_filename})
    else:
        return Response({'status': '404', 'message': 'File not found'})

