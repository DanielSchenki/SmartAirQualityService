# SmartAirQualityService
Python-Webserver with Flask for RaspberryPi 

### `logDHT.py`
This script reads out the GPIO-4-pin of the RaspberryPi to read in the DHT22-Sensor and logs tempereature, humidity and datetime into the `sensors_data.db` sqlite database.
To run this script you have to run following command: `sudo python3 logDHT.py`

### `app.py`
The 'webservice' contains a flask-webservice to fetch data from the sqlite database and represent the data. To run this script you have to run following command: `sudo python3 app.py`
