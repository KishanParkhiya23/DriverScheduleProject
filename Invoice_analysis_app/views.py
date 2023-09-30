from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import subprocess, datetime, os, colorama, sys
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.contrib import messages
from DriverSchedule_app.models import *
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

        # Continue with your subprocess or further processing
        # python_executable = sys.executable
        cmd = ["python","Invoice_analysis_app/utils.py", newFileName]
        subprocess.Popen(cmd,stdout=subprocess.PIPE)  

        if save_data == '1':
            colorama.AnsiToWin32.stream = None
            os.environ["DJANGO_SETTINGS_MODULE"] = "DriverSchedule.settings"      
            cmd = ["python","manage.py", "runscript",'csvToModel.py']
            subprocess.Popen(cmd,stdout=subprocess.PIPE)        
        # colorama.AnsiToWin32.stream = colorama.AnsiToWin32()
        
        # subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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



