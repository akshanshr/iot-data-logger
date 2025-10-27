import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("temperature_log.csv")
data["Timestamp"] = pd.to_datetime(data["Timestamp"])

plt.style.use("seaborn-v0_8-darkgrid")
plt.figure(figsize=(12,6))
plt.plot(data["Timestamp"], data["Temperature (°C)"], color='coral', linewidth=2, label='Temperature')
plt.plot(data["Timestamp"], data["Temperature (°C)"].rolling(5).mean(), color='blue', linestyle='--', label='Trend')

plt.title("Simulated Temperature Data Logger", fontsize=14, fontweight='bold')
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.tight_layout()
plt.savefig("temperature_plot.png")
plt.show()

