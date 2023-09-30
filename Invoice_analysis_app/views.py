from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import subprocess, datetime, os, colorama, sys
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.contrib import messages
from Basic_app.models import *
from Trips_details_app.models import *
from itertools import chain

# --------------------------------------------
# Invoice Analysis
# --------------------------------------------
def index(request):
    return render(request,'Invoice_analysis/get_file.html')

@csrf_protect
@api_view(['POST'])
def invoiceConvert(request):
    invoiceFile = request.FILES.get('csvFile')
    save_data = request.POST.get('save')
    if not invoiceFile:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(invoiceFile.name)
        location = 'static/img/tempInvoice'

        lfs = FileSystemStorage(location=location)
        l_filename = lfs.save(newFileName, invoiceFile)

        cmd = ["python","Invoice_analysis_app/utils.py", newFileName]
        subprocess.Popen(cmd,stdout=subprocess.PIPE)  

        if save_data == '1':
            colorama.AnsiToWin32.stream = None
            os.environ["DJANGO_SETTINGS_MODULE"] = "DriverSchedule.settings"      
            cmd = ["python","manage.py", "runscript",'csvToModel.py']
            subprocess.Popen(cmd,stdout=subprocess.PIPE)        
        messages.success(request, "Please wait 5 minutes. The data conversion process continues")
        return redirect('/')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
    
def DriverEntry(request):
    return render(request , 'Invoice_analysis/driver_entry_file.html')

@csrf_protect
@api_view(['POST'])
def DriverSaveData(request):
    # return HttpResponse('work')
    Driver_csv_file = request.FILES.get('DriverCsvFile')
    if not Driver_csv_file:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(Driver_csv_file.name)
        location = 'static/img/driverRegFile'

        lfs = FileSystemStorage(location=location)
        l_filename = lfs.save(newFileName, Driver_csv_file)
        with open("Driver_reg_file.txt",'w') as f:
            f.write(newFileName)
            f.close()
        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "DriverSchedule.settings"      
        cmd = ["python","manage.py", "runscript",'DriverCsvToModel.py']
        subprocess.Popen(cmd,stdout=subprocess.PIPE)
        messages.success(request, "Please wait 5 minutes. The data conversion process continues")
        return redirect('/')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
    
# --------------------------------------------
# Trip analysis
# --------------------------------------------


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
        basePlants = BasePlant.objects.values_list(
            'basePlantName', flat=True).distinct()
    except:
        basePlants = None

    trucks = list(chain(admin_trucks, client_trucks))
    params['client_names'] = client_names
    params['drivers'] = drivers
    params['trucks'] = trucks
    params['basePlants'] = basePlants
    return render(request, 'admin/analysis.html', params)


@csrf_protect
@api_view(['POST'])
def downloadAnalysis(request):
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    tables = request.POST.getlist('tables[]')
    values = request.POST.getlist('values[]')

    if tables[0] == "all":
        data = DriverTrip.objects.filter(shiftDate__range=[startDate, endDate])
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
                'basePlant': trip.basePlant.basePlant,
                'startTime': trip.startTime,
                'endTime': trip.endTime,
                'logSheet': trip.logSheet,
                'comment': trip.comment
                # Add other fields from the Trip model as needed
            })

        return JsonResponse({'status': True, 'trips': trip_list})

    # print(request.POST,values,tables)

    # return HttpResponse('here')



