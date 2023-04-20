import sys
import time
import sqlite3
import Adafruit_DHT

dbName = 'sensors_data.db'

# frequency => every minute (for now)

sampleFreq = 1 * 10


# fetches data from DHT sensor

def get_DHT_data():
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 4
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)

    if hum is not None and temp is not None:
        temp = round(temp, 3)
        hum = round(hum, 3)
        log_data(temp, hum)


# logs sensor-data on database

def log_data(temp, hum):
    conn = sqlite3.connect(dbName)
    curs = conn.cursor()
    curs.execute("INSERT INTO DHT_DATA VALUES(DATETIME('NOW'), (?), (?))", (temp, hum))
    conn.commit()
    conn.close()


# main function

def main():
    print("start logging data ...")
    while True:
        get_DHT_data()
        time.sleep(sampleFreq)


# ------------ execute program

main()
