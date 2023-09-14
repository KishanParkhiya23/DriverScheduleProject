from background_task import background

# @background(schedule=60)  # Set the desired schedule interval in seconds
def execute_exe_task():
    import execute_task  # Import the custom script

    # Call the function from your custom script
    execute_task.run_exe()
