from datetime import datetime

def get_current_time ():

    # Get the current time
    current_time = datetime.now()

    # Format the time as a string with AM/PM
    time_string = current_time.strftime("%I:%M %p")

    return time_string