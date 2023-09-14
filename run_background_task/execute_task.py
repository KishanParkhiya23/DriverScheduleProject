import subprocess

def run_exe():
    try:
        # Replace 'your_executable.exe' with the actual path to your .exe file
        subprocess.run(['C:/Users/siddhant/Documents/PNR Group/DriverScheduleProject/analysis/test.exe'], check=True)
    except subprocess.CalledProcessError as e:
        # Handle any errors that may occur during execution
        print(f"Error running executable: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     run_exe()
