#!flask/bin/python
from flask import Flask, jsonify
import datetime
import os, csv

app = Flask(__name__)

root=os.getcwd()+'/'
# one run per day at 1 am, hence the file starts from midnight of the same day
run_hour='00'


# here goes the code for computing the current values to be returned
# for the time being this is a stub
currentTarif = "low"
currentDate = datetime.datetime.now()

roundedHour = '00' 
# roundedHour = int(3*round(currentDate.hour/3))
currentDate = currentDate.replace(minute=0, second=0, microsecond=0, hour=int(roundedHour)
# datesArray= []
# for i in range(48):
# 	datesArray.append({"date" : str(currentDate+datetime.timedelta(hours=3*i)), "tarif" : "high"})

# # datesArray =[]
# datesArrayStoro=[]
# datesArraySanLorenzo=[]
# places='Storo','San_Lorenzo']
# root=os.getcwd()+'/'
# run_hour="00"
# for place in places:
# 	current_dir=str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place
# 	signal_file=root+'outputs/'+current_dir+'/signal_'+str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place+'.txt'
# 	# signal_file is effectively a csv file, so we can use csv.py functions
# 	with open(signal_file) as csvfile:
# 		fileReader = csv.reader(csvfile)
# 			for row in fileReader:
# 				datesArray.append({"date" : str(currentDate+datetime.timedelta(row[0])), "tarif" : row[1]})


# code for endpoint implementation

@app.route('/api/tou/storo/current', methods=['GET'])
def get_current_storo():
    return jsonify(tarif=currentTarif)

@app.route('/api/tou/sanlorenzo/current', methods=['GET'])
def get_current_sanlorenzo():
    return jsonify(tarif=currentTarif)

@app.route('/api/tou/storo', methods=['GET'])
def get_storo():
	place='Storo'
	datesArrayStoro=[]
	current_dir=str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place
	signal_file=root+'outputs/'+current_dir+'/signal_'+str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place+'.txt'
	# signal_file is effectively a csv file, so we can use csv.py functions
	# with open(signal_file) as csvfile:
	# 	fileReader = csv.reader(csvfile)
	# 	for row in fileReader:
	# 		datesArrayStoro.append({"date" : str(currentDate+datetime.timedelta(row[0])), "tarif" : row[1]})
    # return jsonify({"data" : datesArrayStoro})

@app.route('/api/tou/sanlorenzo', methods=['GET'])
def get_sanlorenzo():
	place='San_Lorenzo'
	datesArraySanLorenzo=[]
	current_dir=str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place
	signal_file=root+'outputs/'+current_dir+'/signal_'+str(currentDate.day)+'_'+str(currentDate.month)+'_'+str(currentDate.year)+'_'+run_hour+'_'+place+'.txt'
	# signal_file is effectively a csv file, so we can use csv.py functions
	f = open(signal_file, 'r')
	# try:
	fileReader = csv.reader(f)
	for row in fileReader:
		datesArraySanLorenzo.append({"date" : str(currentDate+datetime.timedelta(int(row[0]))), "tarif" : row[1]})
    # finally:
	f.close()
	return jsonify({"data" : datesArraySanLorenzo})
    # return jsonify({"data" : datesArray})

if __name__ == '__main__':
    app.run(debug=True)

    