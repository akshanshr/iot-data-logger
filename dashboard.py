from flask import Flask, render_template_string, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # non-GUI backend for Flask
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>IoT Temperature Dashboard</title>
    <meta http-equiv="refresh" content="10"> <!-- Auto-refresh every 10 sec -->
    <style>
        body {
            background-color: #121212;
            color: #EAEAEA;
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            padding: 30px;
        }
        h1 {
            font-weight: 400;
            color: #00BFFF;
        }
        .card {
            background: #1E1E1E;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            padding: 20px;
            margin: 20px auto;
            width: 80%;
            max-width: 800px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            margin-top: 10px;
            background: #00BFFF;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            transition: 0.3s;
        }
        .btn:hover {
            background: #007acc;
        }
        img {
            width: 100%;
            border-radius: 12px;
        }
    </style>
</head>
<body>
    <h1>🌡 IoT Temperature Data Logger</h1>

    <div class="card">
        <h2>Latest Temperature: {{ latest_temp }} °C</h2>
        <p><strong>Last Recorded:</strong> {{ last_time }}</p>
        <a href="/" class="btn">Refresh Data</a>
    </div>

    <div class="card">
        <h2>Temperature Trend</h2>
        <img src="data:image/png;base64,{{ plot_url }}" alt="Temperature Plot">
    </div>

    <footer style="margin-top:30px; color:#666;">Akshansh Rai & Varundev | IoT Project | Linux + Python</footer>
</body>
</html>
"""

@app.route('/')
def index():
    file_path = 'temperature_log.csv'
    if not os.path.exists(file_path):
        return "<h2>No data logged yet. Run data_logger.py first.</h2>"

    df = pd.read_csv(file_path, names=['time', 'temperature'], header=0 )
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time', 'temperature'])

    # Plot temperature data
    plt.figure(figsize=(8,4))
    plt.plot(df['time'], df['temperature'], color='#00BFFF', linewidth=2)
    plt.title("Temperature over Time", color='white')
    plt.xlabel("Time", color='white')
    plt.ylabel("Temperature (°C)", color='white')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    # Make dark theme
    plt.style.use('dark_background')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    latest_temp = round(df['temperature'].iloc[-1], 2)
    last_time = df['time'].iloc[-1].strftime("%Y-%m-%d %H:%M:%S")

    return render_template_string(TEMPLATE, latest_temp=latest_temp, last_time=last_time, plot_url=plot_data)

if __name__ == '__main__':
    app.run(debug=True)
