from django.shortcuts import render
from django.http import HttpResponse
import subprocess


# Create your views here.

def index(request):
    return render(request,'Invoice_analysis/get_file.html')


def invoiceConvert(request):
    
    cmd = ["python", "utils.py", "arg1"]

    try:
        # Start the subprocess in the background
        subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return HttpResponse("Background process started successfully.")
    except Exception as e:
        return HttpResponse(f"Error starting background process: {str(e)}")

    