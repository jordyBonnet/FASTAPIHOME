"""
Scheduler with a thread that runs every 20 minutes
"""
import threading
from datetime import datetime
import time
import requests

# Event to stop the thread
stop_event = threading.Event()

# daily sports events
has_run_today = False
def daily_sports_events():
    global has_run_today
    # Get the current time
    now = datetime.now()

    # Check if it's past 8:30 AM and the function hasn't run today
    if now.hour >= 8 and now.minute >= 30 and not has_run_today:
        url = f"http://127.0.0.1:8000/daily_sports_events"
        response = requests.get(url)
        print(f'{now.strftime("%d.%m %Hh%M - ")} - {response.json()["message"]}')

        # Set the flag to True so the function won't run again today
        has_run_today = True
    else:
        # Print the current datetime with the format DD MM hh:mm
        print(now.strftime("%d.%m %Hh%M - Waiting for 8:30 AM to run the function"))

    # At midnight, reset the flag
    if now.hour == 0:
        has_run_today = False

# glass trash next day
has_run_today_gtnd = False
def glass_trash_next_day():
    global has_run_today_gtnd
    now = datetime.now()
    # Check if it's past 18 and the function hasn't run today
    if now.hour >= 18 and not has_run_today_gtnd:
        url = f"http://127.0.0.1:8000/glass_trash_day"
        response = requests.get(url)
        print(f'{now.strftime("%d.%m %Hh%M - ")} - {response.json()["message"]}')

        # Set the flag to True so the function won't run again today
        has_run_today_gtnd = True
    else:
        # Print the current datetime with the format DD MM hh:mm
        # print(now.strftime("%d.%m %Hh%M - Waiting for 8:30 AM to run the function"))
        pass

    # At midnight, reset the flag
    if now.hour == 0:
        has_run_today_gtnd = False


def run_thread():
    while not stop_event.is_set():
        daily_sports_events()
        # time.sleep(10)      # Pause for 10 seconds
        glass_trash_next_day()
        time.sleep(60*20)   # Pause for 20 minutes

# Start the thread
thread = threading.Thread(target=run_thread)
thread.start()

# When the main program is about to exit, stop the thread
import atexit
atexit.register(stop_event.set)