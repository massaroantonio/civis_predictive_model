# new function that runs every 24 hours at 4am
import time
import schedule
import library

schedule.every().day.at("4:00").do(library.updateTodayBothPlaces)

while 1:
    schedule.run_pending()
    time.sleep(1)