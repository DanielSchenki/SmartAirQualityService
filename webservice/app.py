import io
# database
import sqlite3
from datetime import datetime
# everything related to the web server
from flask import Flask, render_template, make_response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# everything related to the plot
from matplotlib.figure import Figure

app = Flask(__name__)


# get data from database
def get_last_data():
    time = ""
    temp, hum = (0, 0)
    conn = sqlite3.connect('../sensors_data.db')
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT 1"):
        time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y at %H:%M")
        temp = row[1]
        hum = row[2]
    conn.close()
    if time is not None and temp is not None and hum is not None:
        return time, temp, hum


# get history data from database
def get_hist_data(num_samples):
    conn = sqlite3.connect('../sensors_data.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM DHT_DATA ORDER BY timestamp DESC LIMIT " + str(num_samples))
    data = curs.fetchall()
    dates = []
    temps = []
    hums = []
    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
    conn.close()
    return dates, temps, hums


# test data for cleaning possible "out of range" values
def test_data(temps, hums):
    n = len(temps)
    for i in range(0, n - 1):
        if temps[i] < -10 or temps[i] > 50:
            temps[i] = temps[i - 2]
        if hums[i] < 0 or hums[i] > 100:
            hums[i] = temps[i - 2]
    return temps, hums


# get max number of rows (table size)
def max_rows_table():
    global max_number_rows
    conn = sqlite3.connect('../sensors_data.db')
    curs = conn.cursor()
    for row in curs.execute("SELECT COUNT(temp) FROM  DHT_DATA"):
        max_number_rows = row[0]
    conn.close()
    return max_number_rows


# set number of samples to plot
global num_samples
num_samples = max_rows_table()
if num_samples > 101:
    num_samples = 100


# main route
@app.route("/")
def index():
    time, temp, hum = get_last_data()
    template_data = {
        'time': time,
        'temp': temp,
        'hum': hum
    }
    return render_template('index.html', **template_data)


# main route with POST method
@app.route('/', methods=['POST'])
def my_form_post():
    global num_samples
    num_samples = int(request.form['num_samples'])
    if num_samples > max_number_rows:
        num_samples = max_number_rows
    time, temp, hum = get_last_data()
    template_data = {
        'time': time,
        'temp': temp,
        'hum': hum,
        'num_samples': num_samples
    }
    return render_template('index.html', **template_data)


# route for the temperature plot
@app.route("/plot/temp")
def plot_temp():
    times, temps, hums = get_hist_data(num_samples)
    ys = temps
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.grid(True)
    xs = range(num_samples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


# route for the humidity plot
@app.route("/plot/hum")
def plot_hum():
    times, temps, hums = get_hist_data(num_samples)
    ys = hums
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.grid(True)
    xs = range(num_samples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
