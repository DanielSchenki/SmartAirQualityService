from datetime import datetime
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


# Retrieve data from database
def get_data():
    time = ""
    temp, hum = (0, 0)
    conn = sqlite3.connect('../sensors_data.db')
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT 1"):
        time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y um %H:%M")
        temp = row[1]
        hum = row[2]
    conn.close()
    if time is not None and temp is not None and hum is not None:
        return time, temp, hum


# main route
@app.route("/")
def index():
    time, temp, hum = get_data()
    template_data = {
        'time': time,
        'temp': temp,
        'hum': hum
    }
    return render_template('index.html', **template_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
