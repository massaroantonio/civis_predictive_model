#!flask/bin/python
from flask import Flask, jsonify
import datetime

app = Flask(__name__)

# here goes the code for computing the current values to be returned
# for the time being this is a stub
currentTarif = "low"
currentDate = datetime.datetime.now()
roundedHour = int(3*round(currentDate.hour/3))
currentDate = currentDate.replace(minute=0, second=0, microsecond=0, hour=roundedHour)
datesArray= []
for i in range(48):
	datesArray.append({"date" : str(currentDate+datetime.timedelta(hours=3*i)), "tarif" : "high"})


# code for endpoint implementation

@app.route('/api/tou/storo/current', methods=['GET'])
def get_current_storo():
    return jsonify(tarif=currentTarif)

@app.route('/api/tou/sanlorenzo/current', methods=['GET'])
def get_current_sanlorenzo():
    return jsonify(tarif=currentTarif)

@app.route('/api/tou/storo', methods=['GET'])
def get_storo():
    return jsonify({"data" : datesArray})

@app.route('/api/tou/sanlorenzo', methods=['GET'])
def get_sanlorenzo():
    return jsonify({"data" : datesArray})


if __name__ == '__main__':
    app.run(debug=True)