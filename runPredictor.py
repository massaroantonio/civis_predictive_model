# new function that runs every 5 minutes if it has nott succeded yet

import time
import schedule
import library
from datetime import datetime



schedule.every(1).minutes.do(library.job)

while 1:
    schedule.run_pending()
    time.sleep(1)