from django.http import HttpResponse
import subprocess

# Create your views here.
# In your Django views or wherever you need to trigger the exe
from .tasks import execute_exe_task

def trigger_exe(request):
    # execute_exe_task.delay()
    try:
        # Replace 'your_executable.exe' with the actual path to your .exe file
        subprocess.run(['python','run_background_task/test.py'], check=True)
    except subprocess.CalledProcessError as e:
        # Handle any errors that may occur during execution
        print(f"Error running executable: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
    return HttpResponse("Exe is running in the background.")
