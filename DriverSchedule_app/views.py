from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from .models import *
from rest_framework.decorators import api_view
import shutil
import os
import tabula
import requests
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from itertools import chain
from django.http import JsonResponse


# To call home page
@api_view(['GET'])
def index(request):
    if request.user.is_authenticated:
        return Response({'status': '200', 'message': 'Data Get Successfully', 'form1_data': request.session.get('_auth_user_id')})
    else:
        return render(request, 'index.html')

# TO get all data from driver schedule API


@api_view(['POST'])
@csrf_protect
def getDriverData(request):
    data = {
        'driverschedule': request.POST.get('driverschedule'),
        'startDate': request.POST.get('startDate'),
        'endDate': request.POST.get('endDate'),
    }

    data['startDate'] = (datetime.strptime(
        data['startDate'], "%Y-%m-%d")).strftime("%m-%d-%Y")
    data['endDate'] = (datetime.strptime(
        data['endDate'], "%Y-%m-%d")).strftime("%m-%d-%Y")

    if data['driverschedule'] == 'availability':
        url = "https://www.driverschedule.com/api/schedule"
    elif data['driverschedule'] == 'appointments':
        url = "https://www.driverschedule.com/api/appointments"
    else:
        url = "https://www.driverschedule.com/api/shiftschedulecapacity"

    format_type = "json"
    # Replace with your actual access token
    access_token = "35d0a6c7-db72-4f31-a7f1-f8fbdcef5f00"

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
        client_names = Client.objects.values_list('name', flat=True).distinct()
        admin_truck_no = AdminTruck.objects.values_list(
            'adminTruckNumber', flat=True).distinct()
        client_truck_no = ClientTruckConnection.objects.values_list(
            'clientTruckId', flat=True).distinct()
        sources = Source.objects.values_list(
            'sourceName', flat=True).distinct()
        params = {
            'client_ids': client_names,
            'admin_truck_no': admin_truck_no,
            'client_truck_no': client_truck_no,
            'sources': sources,
        }
        try:
            Driver_  = Driver.objects.get(email=user_email)
            driver_id = str(Driver_) + '-' + str(
                Driver.objects.filter(email=user_email).values_list('name', flat=True)[0])
            params['driver_ids'] = driver_id
            params['drivers'] = None
            DriverTruckNum = Driver_.truckNum.truckNumber
            params['DriverTruckNum'] = DriverTruckNum

            client_names = Client.objects.values_list('name', flat=True)
            params['client_names'] = client_names

            # print(Driver_.truckNum.truckNumber)


        except:
            params['driver_ids'] = None
            drivers = Driver.objects.all()
            params['drivers'] = drivers
            params['DriverTruckNum'] = None
            params['client_names'] = None
            

        return render(request, 'DriverSchedule_app/form1.html', params)

    else:
        return redirect('/admin')


@api_view(['GET'])
def getForm2(request):
    if 'data' in request.session:
        params = {
            'loads': [i+1 for i in range(int(request.session['data'].get('numberOfLoads')))]
        }
        return render(request, 'DriverSchedule_app/form2.html', params)
    else:
        return redirect('DriverSchedule_app:form1')


# @csrf_protect
# @api_view(['POST'])
def createFormSession(request):
    clientName = request.POST.get('clientName')
    logSheet = request.FILES.get('logSheet')
    if logSheet:
        
        load_sheet_folder_path = 'Temp_Load_Sheet'
        fileName = logSheet.name
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        
        log_sheet_new_filename = 'Load_Sheet' + time + \
            '!_@' + fileName.replace(" ", "").replace("\t", "")
            
        lfs = FileSystemStorage(location=load_sheet_folder_path)
        l_filename = lfs.save(log_sheet_new_filename, logSheet)  
              
        data = {
            'driverId': request.POST.get('driverId').split('-')[0],
            'clientName': clientName,
            'truckNum': request.POST.get('truckNum').split('-')[0],
            'startTime': request.POST.get('startTime'),
            'endTime': request.POST.get('endTime'),
            'shiftDate': request.POST.get('shiftDate'),
            'source': request.POST.get('source'),
            'logSheet': log_sheet_new_filename,
            'shiftType': request.POST.get('shiftType'),
            'numberOfLoads': request.POST.get('numberOfLoads'),
            'comments': request.POST.get('comments')
        }

        
        
    data['docketGiven'] = True if Client.objects.get(name = clientName).docketGiven else False
     
    request.session['data'] = data
    request.session.set_expiry(5)
    
    return formsSave(request) if Client.objects.get(name = clientName).docketGiven else redirect('DriverSchedule_app:form2')
   

# @csrf_protect
# @api_view(['POST'])
def formsSave(request):

    driverId = request.session['data']['driverId']
    # driverId = driverId.split('-')[0]
    clientName = request.session['data']['clientName']
    shiftType = request.session['data']['shiftType']
    numberOfLoads = request.session['data']['numberOfLoads']
    truckNo = request.session['data']['truckNum']
    # print(truckNo)
    startTime = request.session['data']['startTime']
    endTime = request.session['data']['endTime']
    source = request.session['data']['source']
    shiftDate = request.session['data']['shiftDate']
    logSheet = request.session['data']['logSheet']
    comment = request.session['data']['comments']
    # return HttpResponse(os.path.exists('Final_Load_Sheet/' + logSheet))
    temp_logSheet = ''
    Docket_no = []
    Docket_file = []
    time = (str(timezone.now())).replace(':', '').replace(
                    '-', '').replace(' ', '').split('.')
    time = time[0]
    
    if not request.session['data']['docketGiven']:
        for i in range(1, int(numberOfLoads)+1):
            
            key = f"docketNumber[{i}]"
            docket_number = request.POST.get(key)
            Docket_no.append(docket_number)
            key_files = f"docketFile[{i}]"
            
            docket_files = request.FILES.get(key_files)

            temp_logSheet = temp_logSheet + '-' + docket_number

            if docket_files:
                
                # return HttpResponse(docket_files.name)
            
                # PDF ---------------
                pdf_folder_path = 'static/img/docketFiles'
                fileName = docket_files.name
                # return HttpResponse(fileName.split('.')[-1])
                docket_new_filename =  time + '!_@' + docket_number + '.' +  fileName.split('.')[-1]
                # return HttpResponse(docket_new_filename)
                pfs = FileSystemStorage(location=pdf_folder_path)
                pfs.save(docket_new_filename, docket_files)
                Docket_file.append(docket_new_filename)


    # temp_logSheet = time + '!_@' + temp_logSheet[1:]
    
    # if not os.path.exists('Final_Load_Sheet/' + logSheet):
    #     shutil.move('Temp_Load_Sheet/' + logSheet, 'Final_Load_Sheet/' + logSheet) 
    
    if not os.path.exists('static/img/finalLogSheet/' + logSheet):
        shutil.move('Temp_Load_Sheet/' + logSheet, 'static/img/finalLogSheet/' + logSheet)
        
    driver = Driver.objects.get(driverId=driverId)
    source = Source.objects.get(sourceName=source)

    trip = Trip(
        driverId=driver,
        clientName=clientName,
        shiftType=shiftType,
        numberOfLoads=numberOfLoads,
        truckNo=truckNo,
        startTime=startTime,
        endTime=endTime,
        logSheet='static/img/finalLogSheet/' + logSheet,  # Use the filename or None
        comment=comment,
        source=source,
        shiftDate=shiftDate
    )
    trip.save()
    
    if not request.session['data']['docketGiven']:
        for i in range(len(Docket_no)):
            docket_ = Docket(
                tripId=trip,
                docketNumber=Docket_no[i],  # Use the specific value from the list
                docketFile='static/img/docketFiles/' + Docket_file[i],  # Use the specific value from the list
            )
            docket_.save()

    del request.session['data']

    messages.success(request, " Form Successfully Filled Up")
    return redirect('/')


def getFileForm(request):
    return render(request, 'DriverSchedule_app/fileForm.html')


@csrf_protect
@api_view(['POST'])
def saveFileForm(request):
    pdf_file = request.FILES.get('pdf_file')

    if pdf_file:

        # PDF ---------------
        pdf_folder_path = 'PDF'
        fileName = pdf_file.name
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        pdf_new_filename = time + '!_@' + \
            fileName.replace(" ", "").replace("\t", "")
        pfs = FileSystemStorage(location=pdf_folder_path)
        p_filename = pfs.save(pdf_new_filename, pdf_file)

        csv_name = pdf_new_filename.replace('.pdf', '.csv')

        # CSV---------------
        tabula.convert_into('PDF/'+pdf_new_filename, "CSV/" +
                            csv_name, output_format="csv", pages='all')

        return Response({'status': '200', 'message': 'Data Get Successfully', 'file': p_filename})
    else:
        return Response({'status': '404', 'message': 'File not found'})


@api_view(['GET'])
def analysisView(request):
    params = {}
    try:
        client_names = Client.objects.values_list('name', flat=True).distinct()
    except:
        client_names = None
    try:
        drivers = Driver.objects.all()
    except:
        drivers = None

    try:
        admin_trucks = AdminTruck.objects.values_list(
            'adminTruckNumber', flat=True).distinct()
    except:
        admin_trucks = None
    try:
        client_trucks = ClientTruckConnection.objects.values_list(
            'clientTruckId', flat=True).distinct()
    except:
        client_trucks = None

    try:
        sources = Source.objects.values_list(
            'sourceName', flat=True).distinct()
    except:
        sources = None

    trucks = list(chain(admin_trucks, client_trucks))
    params['client_names'] = client_names
    params['drivers'] = drivers
    params['trucks'] = trucks
    params['sources'] = sources
    return render(request, 'admin/analysis.html', params)


@csrf_protect
@api_view(['POST'])
def downloadAnalysis(request):
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    tables = request.POST.getlist('tables[]')
    values = request.POST.getlist('values[]')

    if tables[0] == "all":
        data = Trip.objects.filter(shiftDate__range=[startDate, endDate])
        print(data)
        trip_list = []
        for trip in data:
            trip_list.append({
                'shiftDate': trip.shiftDate.strftime('%Y-%m-%d'),
                'driverId': trip.driverId.driverId,
                'clientName': trip.clientName,
                'shiftType': trip.shiftType,
                'numberOfLoads': trip.numberOfLoads,
                'truckNo': trip.truckNo,
                'source': trip.source.sourceName,
                'startTime': trip.startTime,
                'endTime': trip.endTime,
                'logSheet': trip.logSheet,
                'comment': trip.comment
                # Add other fields from the Trip model as needed
            })

        return JsonResponse({'status': True, 'trips': trip_list})

    # print(request.POST,values,tables)

    # return HttpResponse('here')


@csrf_protect
@api_view(['POST'])
def getTrucks(request):
    clientName = request.POST.get('clientName')
    # clientName = request.GET.get('clientName')
    client = Client.objects.get(name=clientName)
    truckList = []
    truck_connections = ClientTruckConnection.objects.filter(
        clientId=client.clientId)
    docket = client.docketGiven

    for truck_connection in truck_connections:
        truckList.append(str(truck_connection.truckNumber) +
                         '-' + str(truck_connection.clientTruckId))
        # print(truck_connection.truckNumber)
        # print(truck_connection.clientTruckId)
    return JsonResponse({'status': True, 'trucks': truckList, 'docket': docket})


@csrf_protect
@api_view(['POST'])
def clientDocket(request):
    clientName = request.POST.get('clientName')
    client = Client.objects.get(name=clientName)
    docket = client.docketGiven
    print(docket)
    return JsonResponse({'status': True, 'docket': docket})


def viewLogSheet(request, logSheet):
    file = 'static/img/finalLogSheet/' + logSheet
    
    try:
        if logSheet.split('.')[-1] == 'pdf':
            with open(file, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
                return response
                # response = FileResponse(pdf_file, content_type='application/pdf')
                # response['Content-Disposition'] = f'inline; filename="{file}"'
                # return response
        elif logSheet.split('.')[-1].lower() == 'jpg' or logSheet.split('.')[-1].lower() == 'jpeg':
            with open(file, 'rb') as image_file:
                # Create an HTTP response with the image content and appropriate content type.
                response = HttpResponse(image_file.read(), content_type='image/jpeg')

                # You can set the Content-Disposition header if needed.
                # response['Content-Disposition'] = f'inline; filename="{image_name}"'

                return response
    except FileNotFoundError:
        return HttpResponse('file_not_found.html')


def viewDocketFile(request, docketFile):
    file = 'static/img/docketFiles/' + docketFile
    
    try:
        if docketFile.split('.')[-1] == 'pdf':
            with open(file, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
                return response
                # response = FileResponse(pdf_file, content_type='application/pdf')
                # response['Content-Disposition'] = f'inline; filename="{file}"'
                # return response
        elif docketFile.split('.')[-1].lower() == 'jpg' or docketFile.split('.')[-1].lower() == 'jpeg':
            with open(file, 'rb') as image_file:
                # Create an HTTP response with the image content and appropriate content type.
                response = HttpResponse(image_file.read(), content_type='image/jpeg')

                # You can set the Content-Disposition header if needed.
                # response['Content-Disposition'] = f'inline; filename="{image_name}"'

                return response
    except FileNotFoundError:
        return HttpResponse('file_not_found.html')