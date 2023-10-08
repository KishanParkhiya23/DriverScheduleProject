
from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from Basic_app.models import *
from Trips_details_app.models import *
from rest_framework.decorators import api_view
import shutil, os,tabula, requests, colorama, subprocess
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from itertools import chain


# To call home page
@api_view(['GET'])
def index(request):
    if request.user.is_authenticated:
        return Response({'status': '200', 'message': 'Data Get Successfully', 'form1_data': request.session.get('_auth_user_id')})
    else:
        return render(request, 'index.html')


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
        basePlant = BasePlant.objects.values_list(
            'basePlant', flat=True).distinct()
        params = {
            'client_ids': client_names,
            'admin_truck_no': admin_truck_no,
            'client_truck_no': client_truck_no,
            'basePlants': basePlant,
        }
        try:
            Driver_  = Driver.objects.get(email=user_email)
            print(Driver_.driverId)
            # driver_id = str(Driver_.driverId) + '-' + str(Driver_.name)   
            # params['driver_ids'] = driver_id
            params['driver_ids'] = Driver_.driverId
            params['drivers'] = None
            # DriverTruckNum = ClientTruckConnection.objects.get(driverId = Driver_.driverId)
            # params['DriverTruckNum'] = str(DriverTruckNum.clientTruckId) + '-' + str(DriverTruckNum.truckNumber)
            # params['client_names'] = str(DriverTruckNum.clientId.name)
            params['DriverTruckNum'] = None
            params['client_names'] = None

        except Exception as e:
            print(e)
            params['driver_ids'] = None
            drivers = Driver.objects.all()
            params['drivers'] = drivers
            params['DriverTruckNum'] = None
            params['client_names'] = None
            

        return render(request, 'Trips_details_app/form1.html', params)

    else:
        return redirect('/admin')


@api_view(['GET'])
def getForm2(request):
    if 'data' in request.session:
        params = {
            'loads': [i+1 for i in range(int(request.session['data'].get('numberOfLoads')))]
        }
        return render(request, 'Trips_details_app/form2.html', params)
    else:
        return redirect('Trips_details_app:form1')


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
            # 'basePlant': request.POST.get('basePlant'),
            'logSheet': log_sheet_new_filename,
            'shiftType': request.POST.get('shiftType'),
            'numberOfLoads': request.POST.get('numberOfLoads'),
            'comments': request.POST.get('comments')
        }

        
        
    data['docketGiven'] = True if Client.objects.get(name = clientName).docketGiven else False
     
    request.session['data'] = data
    # request.session.set_expiry(5)
    
    return formsSave(request) if Client.objects.get(name = clientName).docketGiven else redirect('Trips_details_app:form2')


# @csrf_protect
# @api_view(['POST'])
def formsSave(request):

    driverId = request.session['data']['driverId']
    # driverId = driverId.split('-')[0]
    clientName = request.session['data']['clientName']
    shiftType = request.session['data']['shiftType']
    numberOfLoads = request.session['data']['numberOfLoads']
    truckNo = request.session['data']['truckNum']
    startTime = request.session['data']['startTime']
    endTime = request.session['data']['endTime']
    # basePlant = request.session['data']['basePlant']
    shiftDate = request.session['data']['shiftDate']
    logSheet = request.session['data']['logSheet']
    comment = request.session['data']['comments']
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
    
    if not os.path.exists('static/img/finalLogSheet/' + logSheet):
        shutil.move('Temp_Load_Sheet/' + logSheet, 'static/img/finalLogSheet/' + logSheet)
        
    driver = Driver.objects.get(driverId=driverId)
    basePlant = BasePlant.objects.get(basePlant=basePlant)

    trip = DriverTrip(
        driverId=driver,
        clientName=clientName,
        shiftType=shiftType,
        numberOfLoads=numberOfLoads,
        truckNo=truckNo,
        startTime=startTime,
        endTime=endTime,
        logSheet='static/img/finalLogSheet/' + logSheet,  # Use the filename or None
        comment=comment,
        # basePlant=basePlant,
        shiftDate=shiftDate
    )
    trip.save()
    
    if not request.session['data']['docketGiven']:
        for i in range(len(Docket_no)):
            docket_ = Docket(
                tripId=trip,
                docketNumber=Docket_no[i],  # Use the specific value from the list
                docketFile='static/img/docketFiles/' + Docket_file[i],
                # Use the specific value from the list
            )
            docket_.save()

    del request.session['data']

    messages.success(request, " Form Successfully Filled Up")
    return redirect('/')


def getFileForm(request):
    return render(request, 'Trips_details_app/fileForm.html')


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
    
    
def pastDataEntryView(request):
    return render (request , 'Trips_details_app/past_data_entry.html')

@csrf_protect
@api_view(['POST'])
def pastDataEntrySave(request):
    # return HttpResponse(request.POST.get('dayShift'))
    PastTripFile = request.FILES.get('pastData')
    
    if not PastTripFile:
        return HttpResponse("No file uploaded")
    
    try:
        time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(PastTripFile.name)
        location = 'static/img/pastTripFiles'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, PastTripFile)
        
        with open("pastTripFileName.txt",'w') as f:
            f.write(newFileName)
            f.close()
            
        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "DriverSchedule.settings"      
        cmd = ["python","manage.py", "runscript",'PastDataSave.py']
        subprocess.Popen(cmd,stdout=subprocess.PIPE)
        
        messages.success(request, "Please wait 5 minutes. The data conversion process continues")
        return redirect('/')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
    
    