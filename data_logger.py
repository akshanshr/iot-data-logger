import random
import math
import time
import csv
from datetime import datetime

filename = "temperature_log.csv"

with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["Timestamp", "Temperature (°C)"])

print("Simulated realistic temperature logger started...")

base_temp = 25
angle = 0

try:
    while True:
        # smooth sinusoidal variation (like daily temp pattern)
        temperature = base_temp + math.sin(angle) * 5 + random.uniform(-0.5, 0.5)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, round(temperature, 2)])

        print(f"{timestamp} -> {temperature:.2f}°C")

        angle += 0.1
        time.sleep(5)

except KeyboardInterrupt:
    print("\nLogging stopped by user.")

