from flask import Flask, jsonify, render_template
import random
import time
import threading

app = Flask(__name__)

latest_temp = None

# Background thread function
def generate_temperature():
    global latest_temp
    while True:
        latest_temp = round(random.uniform(20.0, 35.0), 2)
        print("Generated:", latest_temp)
        time.sleep(5)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def data():
    return jsonify({"temperature": latest_temp})


# Start background thread
if __name__ == "__main__":
    t = threading.Thread(target=generate_temperature)
    t.daemon = True
    t.start()
    app.run(host="0.0.0.0", port=10000)
else:
    # ✅ Important so Render runs temperature generator
    t = threading.Thread(target=generate_temperature)
    t.daemon = True
    t.start()

