# import modules
import http.client
import sqlite3
import time
import urllib
from datetime import datetime


# get data from database
def get_last_data():
    time = ""
    temp, hum = (0, 0)
    conn = sqlite3.connect('sensors_data.db')
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT 1"):
        time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y at %H:%M")
        temp = row[1]
        hum = row[2]
    conn.close()
    if time is not None and temp is not None and hum is not None:
        return time, temp, hum


# send notification to mobile device
def send_notification():
    time, temp, hum = get_last_data()

    # create connection
    conn = http.client.HTTPSConnection("api.pushover.net:443")

    # send notification
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": "ag1hneaetxity8e76xnei21q77tvfp",
                     "user": "uz8z9ruvvxyuwh1v24h228r4ywffnn",
                     "title": "SmartAirQualityService",
                     "message": "Temperature: " + str(temp) + "°C, Humidity: " + str(hum) + "%",
                 }), {"Content-type": "application/x-www-form-urlencoded"})

    # get response
    conn.getresponse()


# main function
def main():
    while True:
        send_notification()
        time.sleep(14400)


main()
