This project was developed as part of the EC-sponsored CIVIS Project (http://www.civisproject.eu/).
It includes a backend service, accessible through REST APIs, for the computation of a dynamic time-of-usage tariffing scheme for the
pilot sites of Storo and San Lorenzo.

The project logically consists of two parts:
1. a prediction engine that runs every 24 hours at 4am (local time), polls NOAA for weather prediction data and computes the tariffing scheme 
for the next 48 hours
2. a set of REST APIs for interaction with the CIVIS app

The project is written mostly in Python (compatibility checked for 2.7.x). It requires the schedule package, which can be installed by
$ pip install schedule

The first part can be started launching startPredictor.sh.
