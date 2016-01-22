#!flask/bin/python
from flask import Flask, jsonify
import datetime
import os, csv, sys
import numpy as np

app = Flask(__name__)
# from app import app

#root=os.getcwd()+'/'
root='/home/ubuntu/civis_predictive_model/'
# # one run per day at 3 am, hence the file starts from midnight of the same day
run_hour='00'


# # here goes the code for computing the current values to be returned
# # for the time being this is a stub
# currentTarif = "low"
currentDate = datetime.datetime.now()
# currentDate=datetime.datetime(2015,12,11)


roundedHour = '00'
# # roundedHour = int(3*round(currentDate.hour/3))
currentDate = currentDate.replace(minute=0, second=0, microsecond=0, hour=int(roundedHour))
# added for debugging purpose, just to make sure the corresponding output file is there
# currentDate=datetime.datetime(2015,12,11)
# this is a stub
# currentTarif="high"


# datesArray= []
# for i in range(48):
#       datesArray.append({"date" : str(currentDate+datetime.timedelta(hours=3*i)), "tarif" : "high"})

# # datesArray =[]
# datesArrayStoro=[]
# datesArraySanLorenzo=[]
# places='Storo','San_Lorenzo']
# root=os.getcwd()+'/'
# run_hour="00"
# for place in places:
#       current_dir=str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place
#       signal_file=root+'outputs/'+current_dir+'/signal_'+str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place+'.txt'
#       # signal_file is effectively a csv file, so we can use csv.py functions
#       with open(signal_file) as csvfile:
#               fileReader = csv.reader(csvfile)
#                       for row in fileReader:
#                               datesArray.append({"date" : str(currentDate+datetime.timedelta(row[0])), "tarif" : row[1]})

#note: the data relative to the current date must be already available for the function to give outputm otherwise it outputs a warning
def get_nearest_value(place,givenDate):
    y=givenDate.year
    m=givenDate.month
    d=givenDate.day
    h=givenDate.hour
    mydir=str(d)+'_'+str(m)+'_'+str(y)+'_00_'+place
    myfile='signal_'+str(d)+'_'+str(m)+'_'+str(y)+'_00_'+place+'.txt'
    output_dir=root+'outputs/'
    assert mydir in os.listdir(output_dir) ,'the forecast for the current day and place has not been run yet'
    assert myfile in os.listdir(output_dir+mydir), 'missing signal file'
    f=open(output_dir+mydir+'/'+myfile)
    time=np.array([int(l.split(',')[0]) for l in f])
    f.seek(0)
    signal=[l.split(',')[1] for l in f]
    return signal[np.argmin(np.abs(time-h))][:-1]
# gets the nearest ToU value for the current date and for a given place (it is a simple wrapper of get_nearest_value above)
def get_nearest_value_now(place):
    now=datetime.now()
    return get_nearest_value(place,now)

# code for endpoint implementation




@app.route('/api/tou/storo/current', methods=['GET'])
def get_current_storo():
        return jsonify(tarif=get_nearest_value('Storo',currentDate))

@app.route('/api/tou/sanlorenzo/current', methods=['GET'])
def get_current_sanlorenzo():
    return jsonify(tarif=get_nearest_value('San_Lorenzo',currentDate))

@app.route('/api/tou/storo', methods=['GET'])
def get_storo():
        place='Storo'
        datesArrayStoro=[]
        current_dir=str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place
        output_dir=root+'outputs/'
        assert current_dir in os.listdir(output_dir) ,'the forecast for the current day and place has not been run yet'
        signal_file=root+'outputs/'+current_dir+'/signal_'+str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place+'.txt'
        f = open(signal_file, 'r')
        # try:
        fileReader = csv.reader(f)
        for row in fileReader:
                #edited by Antonio Massaro: timedelta(n) increases by n days, timedelta (0,m) increases by m seconds
                #datesArrayStoro.append({"date" : str(currentDate+datetime.timedelta(int(row[0]))), "tarif" : row[1]})
                datesArrayStoro.append({"date" : str(currentDate+datetime.timedelta(0,3600*int(row[0]))), "tarif" : row[1]})
    # finally:
        f.close()
        return jsonify({"data" : datesArrayStoro})
        
@app.route('/api/tou/sanlorenzo', methods=['GET'])
def get_sanlorenzo():
        place='San_Lorenzo'
        datesArraySanLorenzo=[]
        current_dir=str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place
        output_dir=root+'outputs/'
        assert current_dir in os.listdir(output_dir) ,'the forecast for the current day and place has not been run yet'
        signal_file=root+'outputs/'+current_dir+'/signal_'+str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place+'.txt'
        # signal_file is effectively a csv file, so we can use csv.py functions
        f = open(signal_file, 'r')
        # try:
        fileReader = csv.reader(f)
        for row in fileReader:
                #edited by Antonio Massaro: timedelta(n) increases by n days, timedelta (0,m) increases by m seconds
                #datesArrayStoro.append({"date" : str(currentDate+datetime.timedelta(int(row[0]))), "tarif" : row[1]})
                datesArraySanLorenzo.append({"date" : str(currentDate+datetime.timedelta(0,3600*int(row[0]))), "tarif" : row[1]})
    # finally:
        f.close()
        return jsonify({"data" : datesArraySanLorenzo})
    # return jsonify({"data" : datesArray})

if __name__ == '__main__':
    app.run(debug=True)

