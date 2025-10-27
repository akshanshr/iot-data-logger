from flask import Flask, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# In-memory storage (List of dictionaries)
temperature_data = []

@app.route('/data')
def data():
    temp = round(random.uniform(20, 35), 2)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    temperature_data.append({"time": now, "temperature": temp})

    # Keep only last 100 entries to avoid excess memory usage
    temperature_data[:] = temperature_data[-100:]

    return jsonify({"time": now, "temperature": temp})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

