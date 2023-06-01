import time
import sqlite3
import Adafruit_DHT

dbName = 'sensors_data.db'

# frequency => every minute (for now)
sampleFreq = 1 * 10


# fetches data from DHT sensor
def get_dht_data():
    dht22_sensor = Adafruit_DHT.DHT22
    dht_pin = 4
    hum, temp = Adafruit_DHT.read_retry(dht22_sensor, dht_pin)

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
        get_dht_data()
        time.sleep(sampleFreq)


# ------------ execute program
main()
