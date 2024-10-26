import requests
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.losses import MeanSquaredError
import os
from datetime import datetime, timedelta

WEATHER_API_KEY = '5465bc7d107d41f9a01162729242510'
GEOCODE_API_KEY = 'ce9cf096220d40458d0e3b2502573bf0'
BASE_WEATHER_URL = 'http://api.weatherapi.com/v1/current.json'
BASE_GEOCODE_URL = 'https://api.opencagedata.com/geocode/v1/json'

# Fetch today's weather for a given zone
def get_current_weather(zone):
    response = requests.get(f"{BASE_GEOCODE_URL}?q={zone}&key={GEOCODE_API_KEY}")
    data = response.json()

    if response.status_code != 200 or not data['results']:
        print("Location not found.")
        return None

    lat = data['results'][0]['geometry']['lat']
    lon = data['results'][0]['geometry']['lng']

    weather_response = requests.get(f"{BASE_WEATHER_URL}?q={lat},{lon}&key={WEATHER_API_KEY}")
    weather_data = weather_response.json()

    if weather_response.status_code != 200:
        print("Failed to retrieve current weather data.")
        return None

    current_weather = {
        'temperature': weather_data['current']['temp_c'],
        'pressure': weather_data['current']['pressure_mb'],
        'humidity': weather_data['current']['humidity'],
        'wind_speed': weather_data['current']['wind_kph']
    }
    return current_weather

# Load model
def load_model():
    return tf.keras.models.load_model("weatherlstm.h5", custom_objects={"mse": MeanSquaredError()})

# Retrain model if not available
def retrain_model(synthetic_data, time_steps=60, epochs=10):
    X, y = prepare_training_data(synthetic_data, time_steps)
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])),
        Dense(4)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=epochs, batch_size=32, verbose=1)
    model.save("weatherlstm.h5")
    return model

# Create synthetic data
def create_synthetic_data(today_weather, num_samples=720):
    np.random.seed(0)
    synthetic_data = pd.DataFrame({
        'temperature': np.random.normal(loc=today_weather['temperature'], scale=5, size=num_samples),
        'pressure': np.random.normal(loc=today_weather['pressure'], scale=2, size=num_samples),
        'humidity': np.random.normal(loc=today_weather['humidity'], scale=8, size=num_samples),
        'wind_speed': np.random.normal(loc=today_weather['wind_speed'], scale=3, size=num_samples)
    })
    synthetic_data['humidity'] = synthetic_data['humidity'].clip(lower=0, upper=100)
    synthetic_data['wind_speed'] = synthetic_data['wind_speed'].clip(lower=0)
    return synthetic_data

# Prepare training data
def prepare_training_data(synthetic_data, time_steps=60):
    X, y = [], []
    for i in range(len(synthetic_data) - time_steps):
        X.append(synthetic_data.iloc[i:i + time_steps].values)
        y.append(synthetic_data.iloc[i + time_steps].values)
    return np.array(X), np.array(y)

# Forecast using LSTM model
def forecast_future(normalized_data, model, scaler):
    input_data = normalized_data[-60:]
    input_data = input_data.reshape((1, input_data.shape[0], input_data.shape[1]))

    forecast = []
    for _ in range(5 * 144):  # Forecast 5 days with 10-minute intervals
        pred = model.predict(input_data)
        forecast.append(pred)
        input_data = np.append(input_data[:, 1:, :], pred.reshape(1, 1, -1), axis=1)

    # Rescale forecasted data back to original values
    forecast = scaler.inverse_transform(np.array(forecast).reshape(-1, normalized_data.shape[1]))
    return forecast

# Determine best irrigation day from forecast and display results
def find_best_irrigation_day(forecast_df):
    temp_min_threshold = 20
    temp_max_threshold = 26
    humidity_min_threshold = 45
    humidity_max_threshold = 70
    wind_speed_max_threshold = 25

    best_day = None
    print("\n5-Day Weather Forecast and Irrigation Suitability:")

    for day, day_data in forecast_df.resample('D'):
        avg_temp = day_data['temperature'].mean()
        avg_humidity = day_data['humidity'].mean()
        max_wind_speed = day_data['wind_speed'].max()

        meets_conditions = (temp_min_threshold <= avg_temp <= temp_max_threshold and
                            humidity_min_threshold <= avg_humidity <= humidity_max_threshold and
                            max_wind_speed <= wind_speed_max_threshold)
        
        suitability = "Suitable" if meets_conditions else "Not Suitable"
        print(f"{day.date()}: Avg Temp: {avg_temp:.2f}°C, Avg Humidity: {avg_humidity:.2f}%, "
              f"Max Wind Speed: {max_wind_speed:.2f} m/s - {suitability}")

        if meets_conditions and best_day is None:
            best_day = day.date()

    return best_day

# Main function
if __name__ == "__main__":
    zone = input("Please enter a location: ")
    today_weather = get_current_weather(zone)
 
    if today_weather:
        synthetic_data = create_synthetic_data(today_weather)

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(synthetic_data)

        model = load_model() if os.path.exists("weatherlstm.h5") else retrain_model(synthetic_data)

        forecast_data = forecast_future(scaled_data, model, scaler)
        forecast_dates = pd.date_range(start=datetime.now(), periods=720, freq='10min')
        forecast_df = pd.DataFrame(forecast_data, columns=['temperature', 'pressure', 'humidity', 'wind_speed'], index=forecast_dates)

        best_day = find_best_irrigation_day(forecast_df)
        if best_day:
            print(f"\nBest day to irrigate: {best_day}")
        else:
            print("\nNo optimal day for irrigation found in the next 5 days.")
