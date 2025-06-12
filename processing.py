import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("aitoma-flood-multisensor.csv", parse_dates=["timestamp"])
df.set_index("timestamp", inplace=True)

locations = ["Gunungsari", "Jagir Kalimir", "Dinoyo", "Jambangan", "Pintu Air Wonokromo"]
custom_thresholds = {
    "Gunungsari": {"normal": 3.2, "flood": 2.9, "critical": 2.0},
    "Jagir Kalimir": {"normal": 3.1, "flood": 2.85, "critical": 1.9},
    "Dinoyo": {"normal": 3.25, "flood": 2.8, "critical": 2.1},
    "Jambangan": {"normal": 3.3, "flood": 2.95, "critical": 2.2},
    "Pintu Air Wonokromo": {"normal": 3.15, "flood": 2.9, "critical": 2.0}
}

for loc in locations:
    plt.figure(figsize=(12, 10))
    
    plt.subplot(4, 1, 1)
    df[f"{loc}_water_level"].plot(label="Water Level")

    # Tambahkan garis threshold per lokasi
    threshold = custom_thresholds[loc]
    plt.axhline(y=threshold["normal"], color="green", linestyle="--", label="Normal Threshold")
    plt.axhline(y=threshold["flood"], color="orange", linestyle="--", label="Flood Threshold")
    plt.axhline(y=threshold["critical"], color="red", linestyle="--", label="Critical Threshold")

    plt.title(f"{loc} - Water Level")
    plt.ylabel("Meter")
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 1, 2)
    df[f"{loc}_temperature_c"].plot(color='orange')
    plt.title(f"{loc} - Temperature")
    plt.ylabel("°C")
    plt.grid(True)

    plt.subplot(4, 1, 3)
    df[f"{loc}_rainfall_mm"].plot(color='blue')
    plt.title(f"{loc} - Rainfall")
    plt.ylabel("mm")
    plt.grid(True)

    plt.subplot(4, 1, 4)
    df[f"{loc}_humidity_percent"].plot(color='green')
    plt.title(f"{loc} - Humidity")
    plt.ylabel("%")
    plt.xlabel("Time")
    plt.grid(True)

    plt.tight_layout()
    plt.show()
