# Standard
import time
from datetime import datetime
# Custom
import Log
log = Log.logger

# Polling frequency in seconds
def wait_until(correct_dt, polling_frequency=10):
    time_to_start = False
    while not time_to_start:
        if datetime.now().time() >= datetime.strptime(correct_dt, '%H:%M:%S').time():
            log.info('Time to start the process')
            return True
        log.info('Waiting for correct dayTime (until ' + correct_dt + ')...')
        time.sleep(polling_frequency)
