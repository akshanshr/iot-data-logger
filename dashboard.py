from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import requests

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>IoT Temperature Dashboard</title>
    <style>
        body { background: #111; color: #eee; font-family: Arial; text-align: center; padding: 20px; }
        .card { background: #1c1c1c; padding: 20px; margin: 10px auto; width: 85%; border-radius: 10px; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; }
        img { width: 100%; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>🌡 IoT Temperature Data Logger</h1>
    <div class="card">
        <h2>Latest Temperature: {{ latest_temp }} °C</h2>
        <p>Last Recorded: {{ last_time }}</p>
        <a href="/" class="btn">Refresh Data</a>
    </div>
    <div class="card">
        <h3>Temperature Trend</h3>
        <img src="data:image/png;base64,{{ plot_url }}" alt="Temperature Plot">
    </div>
</body>
</html>
"""

def fetch_data():
    try:
        res = requests.get("https://iot-data-logger.onrender.com/data")
        return res.json()
    except:
        return None

@app.route('/')
def index():
    data_points = []
    for _ in range(10):
        d = fetch_data()
        if d:
            data_points.append(d)

    df = pd.DataFrame(data_points)

    if df.empty:
        return "<h2>No data received from server.</h2>"

    df['time'] = pd.to_datetime(df['time'])
    plt.style.use('dark_background')
    plt.figure(figsize=(8,4))
    plt.plot(df['time'], df['temperature'], linewidth=2)
    plt.title("Temperature Trend")
    plt.xlabel("Time")
    plt.ylabel("Temp °C")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    latest = df.iloc[-1]
    return render_template_string(TEMPLATE, latest_temp=latest['temperature'], last_time=str(latest['time']), plot_url=plot_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
