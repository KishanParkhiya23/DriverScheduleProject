from django.shortcuts import render
from django.http import HttpResponse
import subprocess, datetime, os, colorama
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages

import sys


# Create your views here.

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