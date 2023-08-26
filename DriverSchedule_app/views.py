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
    params = {}
    if request.user.is_authenticated:
        user_email = request.user.email
                  

        # return HttpResponse(Driver.objects.values_list('driverId', flat=True))
        client_names = Client.objects.values_list('name', flat=True).distinct() 
        admin_truck_no = AdminTruck.objects.values_list('adminTruckNumber', flat=True).distinct()
        client_truck_no = ClientTruckConnection.objects.values_list('clientTruckId', flat=True).distinct()
        sources = Source.objects.values_list('sourceName', flat=True).distinct()
        params = {
            'client_ids' : client_names,
            'admin_truck_no' : admin_truck_no,
            'client_truck_no' : client_truck_no,
            'sources':sources,
            }
        try:
            driver_id = str(Driver.objects.get(email=user_email)) +'-' +  str(Driver.objects.filter(email = user_email).values_list('name', flat=True)[0])
            params['driver_ids'] = driver_id
            params['drivers'] = None
        except:
            params['driver_ids'] = None
            drivers = Driver.objects.all()
            params['drivers'] = drivers
            
      
        return render(request, 'DriverSchedule_app/form1.html', params)

    else:
        return redirect('/admin')

@api_view(['GET'])
def getForm2(request):
    if 'data' in request.session:
        params = {        
            'loads' :[i+1 for i in range(int( request.session['data'].get('numberOfLogs')))]
        } 
        return render(request,'DriverSchedule_app/form2.html',params)
    else:
        return redirect('DriverSchedule_app:form1')


@csrf_protect
@api_view(['POST'])
def createFormSession(request):
    
    logSheet = request.FILES.get('logSheet')


    if logSheet:
        load_sheet_folder_path = 'Temp_Load_Sheet'
        fileName = logSheet.name
        time = (str(timezone.now())).replace(':','').replace('-','').replace(' ','').split('.')
        time = time[0]
        log_sheet_new_filename ='Load_Sheet'+ time + '!_@' + fileName.replace(" ", "").replace("\t", "") 
        lfs = FileSystemStorage(location=load_sheet_folder_path)
        l_filename = lfs.save(log_sheet_new_filename, logSheet)
        data = {
            'driverId':request.POST.get('driverId'),
            'clientName':request.POST.get('clientName'),
            'truckNum':request.POST.get('truckNum'),
            'startTime':request.POST.get('startTime'),
            'endTime':request.POST.get('endTime'),
            'shiftDate':request.POST.get('shiftDate'),
            'source':request.POST.get('source'),
            'logSheet':log_sheet_new_filename,
            'shiftType':request.POST.get('shiftType'),
            'numberOfLogs':request.POST.get('numberOfLogs'),
            'comments':request.POST.get('comments')
        }
        
        request.session['data']= data
        
        # with open('extra.txt','a') as f:
        #     f.writelines(data)
        #     f.close()
        
    request.session.set_expiry(60 *5)
    return redirect ('DriverSchedule_app:form2')
        

        
@csrf_protect
@api_view(['POST'])
def formsSave(request):
    
    driverId = request.session['data']['driverId']   
    driverId = driverId.split('-')[0]
    clientName = request.session['data']['clientName'] 
    shiftType = request.session['data']['shiftType']
    numberOfLog = request.session['data']['numberOfLogs']
    truckNo = request.session['data']['truckNum']             
    startTime = request.session['data']['startTime']    
    endTime = request.session['data']['endTime']    
    source = request.session['data']['source']    
    shiftDate = request.session['data']['shiftDate']    
    logSheet = request.session['data']['logSheet']    
    comment = request.session['data']['comments']    
    
    temp_logSheet = ''
    Docket_no = []
    Docket_file = []
   
    for i in range(1,int(numberOfLog)+1):
        key = f"docketNumber[{i}]"
        docket_number = request.POST.get(key)
        Docket_no.append(docket_number)
        key_files = f"docketFile[{i}]"
        docket_files = request.FILES.get(key_files)

        temp_logSheet = temp_logSheet + '-' + docket_number

        if docket_files:
            # Specify the folder path where you want to save the file
            
            # PDF ---------------
            pdf_folder_path = 'Docket_File'
            fileName = docket_files.name
            time = (str(timezone.now())).replace(':','').replace('-','').replace(' ','').split('.')
            time = time[0]
            docket_new_filename = time + '!_@' + docket_number 
            pfs = FileSystemStorage(location=pdf_folder_path)
            pfs.save(docket_new_filename, docket_files)
            Docket_file.append(docket_new_filename)
        
    temp_logSheet =  time + '!_@' + temp_logSheet[1:]
    shutil.move('Temp_Load_Sheet/' + logSheet, 'Final_Load_Sheet/'+temp_logSheet) if not os.path.exists('Final_Load_Sheet/' + temp_logSheet) else None
    driver = Driver.objects.get(driverId=driverId)
    source = Source.objects.get(sourceName=source)
    

    trip = Trip(
        driverId=driver,
        clientName=clientName,
        shiftType=shiftType,
        numberOfLog=numberOfLog,
        truckNo=truckNo,
        startTime=startTime,
        endTime=endTime,
        logSheet=temp_logSheet,  # Use the filename or None
        comment=comment,
        source = source,
        shiftDate = shiftDate
    )
    # print(source)
    # return HttpResponse(source)
    trip.save()
            
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

def analysis(request):
    return render(request,'admin/analysis.html')