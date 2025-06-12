import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import matplotlib.pyplot as plt

df = pd.read_csv("aitoma-flood-multisensor.csv", parse_dates=["timestamp"])
df.set_index("timestamp", inplace=True)

loc = "Gunungsari"

df["water_level_next"] = df[f"{loc}_water_level"].shift(-1)

features = [
    f"{loc}_water_level",
    f"{loc}_rainfall_mm",
    f"{loc}_temperature_c",
    f"{loc}_humidity_percent"
]

df_model = df[features + ["water_level_next"]].dropna()

X = df_model[features]
y = df_model["water_level_next"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = XGBRegressor(n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))

plt.figure(figsize=(14, 6))
plt.plot(y_test.values, label="Aktual", alpha=0.7)
plt.plot(y_pred, label="Prediksi", alpha=0.7)
plt.title(f"Prediksi Water Level - {loc} (RMSE: {rmse:.4f})")
plt.xlabel("Waktu (index sample)")
plt.ylabel("Water Level (m)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
