import os
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

# Step 1: Generate synthetic weather data
def generate_synthetic_weather_data(num_days=60):
    start_date = pd.Timestamp('2023-01-01')
    date_rng = pd.date_range(start=start_date, end=start_date + pd.Timedelta(days=num_days), freq='10T')
    temperature = np.random.uniform(low=10, high=35, size=len(date_rng))
    pressure = np.random.uniform(low=950, high=1050, size=len(date_rng))
    humidity = np.random.uniform(low=0, high=100, size=len(date_rng))
    wind_speed = np.random.uniform(low=3, high=20, size=len(date_rng))
    
    weather_data = pd.DataFrame({
        'date_time': date_rng,
        'temperature': temperature,
        'pressure': pressure,
        'humidity': humidity,
        'wind_speed': wind_speed
    })
    weather_data.set_index('date_time', inplace=True)
    return weather_data

# Generate synthetic data
raw_data = generate_synthetic_weather_data(num_days=60)

# Step 2: Preprocess the data
def preprocess_data(raw_data):
    mean = raw_data.mean(axis=0)
    std = raw_data.std(axis=0)
    normalized_data = (raw_data - mean) / std
    return normalized_data, mean, std

normalized_data, mean, std = preprocess_data(raw_data)

# Step 3: Prepare Training Sequences for LSTM
def create_sequences(data, seq_length=720):
    sequences, labels = [], []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i+seq_length])
        labels.append(data[i+seq_length])
    return np.array(sequences), np.array(labels)

seq_length = 720
train_sequences, train_labels = create_sequences(normalized_data.values, seq_length)

# Model filename
model_filename = "weather.h5"

# Step 4: Build, Compile, and Train the Complex LSTM Model
def build_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(100, activation='relu', return_sequences=True, input_shape=input_shape),
        tf.keras.layers.LSTM(100, activation='relu', return_sequences=True),
        tf.keras.layers.LSTM(50, activation='relu'),
        tf.keras.layers.Dense(4)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Load or train the model
if os.path.exists(model_filename):
    model = tf.keras.models.load_model(model_filename, custom_objects={'mse': tf.keras.losses.MeanSquaredError()})
    print("Model loaded from file.")
else:
    model = build_model((seq_length, 4))
    history = model.fit(train_sequences, train_labels, epochs=50, batch_size=32, validation_split=0.2)
    model.save(model_filename)
    print("Model trained and saved to file.")

    # Optional: Plot loss to verify training quality
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.show()

# Step 5: Forecast Function for Future Use
def forecast_future(data, model, steps=720):
    forecast = []
    input_data = data[-seq_length:]

    for _ in range(steps):
        input_data = input_data.reshape((1, seq_length, 4))
        prediction = model.predict(input_data)
        forecast.append(prediction[0])
        
        input_data = np.append(input_data[:, 1:, :], [prediction], axis=1)
    
    forecast = np.array(forecast)
    forecast = forecast * std.values + mean.values  # Denormalize the forecast
    return forecast

# Save the forecasting function to a file for future use
with open('forecast_function.py', 'w') as f:
    f.write('''
import numpy as np

def forecast_future(data, model, steps=720, seq_length=720):
    forecast = []
    input_data = data[-seq_length:]

    for _ in range(steps):
        input_data = input_data.reshape((1, seq_length, 4))
        prediction = model.predict(input_data)
        forecast.append(prediction[0])
        
        input_data = np.append(input_data[:, 1:, :], [prediction], axis=1)
    
    return np.array(forecast)
    ''')

print("Forecast function saved to 'forecast_function.py'.")

