# new function that runs every 24 hours at 1am
import time
import schedule
import library

schedule.every().day.at("1:00").do(library.updateTodayBothPlaces)

while 1:
    schedule.run_pending()
    time.sleep(1)