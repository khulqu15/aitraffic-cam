import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

start_time = datetime(2025, 4, 8, 16, 4, 0)
end_time = start_time + timedelta(days=30)
interval = timedelta(seconds=5)

locations = {
    "Gunungsari": {"elevation": 5.0},
    "Jagir Kalimir": {"elevation": 4.0},
    "Dinoyo": {"elevation": 4.0},
    "Jambangan": {"elevation": 6.0},
    "Pintu Air Wonokromo": {"elevation": 4.5}
}

thresholds = {
    "normal_min": 3.0,
    "normal_max": 3.3,
    "flood_min": 2.8,
    "flood_max": 3.1,
    "critical": 1.96
}

def generate_advanced_random_series(length, base, amplitude, freq=0.001, noise_level=0.005):
    t = np.linspace(0, length, length)
    
    seasonal = amplitude * np.sin(2 * np.pi * freq * t)
    random_walk = np.cumsum(np.random.normal(loc=0.0, scale=noise_level, size=length))
    noise = np.random.normal(loc=0.0, scale=noise_level, size=length)
    raw_data = base + seasonal + random_walk + noise

    return np.clip(raw_data / 1.4, 1.5, 8.0)


def generate_rainfall_series(length):
    rainfall = []
    for i in range(length):
        hour = (i * 5 // 3600) % 24
        is_raining = (hour >= 14 and hour <= 17) or (hour >= 2 and hour <= 4)
        rain = np.random.gamma(1.2, 0.8) if is_raining and random.random() < 0.15 else 0.0
        rainfall.append(rain)
    return np.clip(np.array(rainfall), 0, None)

def generate_temperature_series(length):
    t = np.linspace(0, length, length)
    base_temp = 31
    daily_cycle = 2.5 * np.sin(2 * np.pi * t / (86400 / 5))
    weekly_cycle = 1.0 * np.sin(2 * np.pi * t / (604800 / 5))
    noise = np.random.normal(0, 0.8, size=length)
    spikes = np.random.choice([0, 1], size=length, p=[0.995, 0.005]) * np.random.normal(3, 1, size=length)
    return np.clip(base_temp + daily_cycle + weekly_cycle + noise + spikes, 0, None)

def generate_humidity_series(length):
    t = np.linspace(0, length, length)
    base_hum = 75
    daily_cycle = 6 * np.sin(2 * np.pi * t / (86400 / 5))
    weekly_cycle = 3 * np.sin(2 * np.pi * t / (604800 / 5))
    noise = np.random.normal(0, 2.5, size=length)
    spikes = np.random.choice([0, 1], size=length, p=[0.99, 0.01]) * np.random.normal(10, 5, size=length)
    return np.clip(base_hum + daily_cycle + weekly_cycle + noise + spikes, 0, 100)

timestamps = []
current = start_time
while current <= end_time:
    timestamps.append(current)
    current += interval

data = {"timestamp": timestamps}
length = len(timestamps)

for loc in locations:
    base_level = random.uniform(thresholds["normal_min"], thresholds["normal_max"])
    data[f"{loc}_water_level"] = generate_advanced_random_series(length, base_level, amplitude=0.15)
    data[f"{loc}_temperature_c"] = generate_temperature_series(length)
    data[f"{loc}_rainfall_mm"] = generate_rainfall_series(length)
    data[f"{loc}_humidity_percent"] = generate_humidity_series(length)

df = pd.DataFrame(data)
df.to_csv("aitoma-flood-multisensor.csv", index=False)
print("Data berhasil disimpan dalam 'aitoma-flood-multisensor.csv'")
