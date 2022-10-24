# Standard
import time
from datetime import datetime

from Log import Log

Log = Log.get_instance()


def until(correct_dt):
    time_to_start = False
    while not time_to_start:
        if datetime.now().time() >= datetime.strptime(correct_dt, '%H:%M:%S').time():
            Log.info('Time to start the process')
            time_to_start = True
            return True
        Log.info('Waiting for correct dayTime (until ' + correct_dt + ')...')
        time.sleep(10)
