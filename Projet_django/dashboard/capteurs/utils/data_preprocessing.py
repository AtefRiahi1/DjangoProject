import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datasets import load_dataset

def preprocess_data(data, sequence_length=12):
    # Use only the relevant features
    features = data[['Absolute maximum temperature [°C]', 
                     'Absolute minimum temperature [°C]', 
                     'Average monthly temperature [°C]']]

    # Scale the data to [0, 1] for better LSTM performance
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)

    # Prepare sequences for LSTM
    X, y = [], []
    for i in range(len(features_scaled) - sequence_length):
        X.append(features_scaled[i:i + sequence_length])
        y.append(features_scaled[i + sequence_length, 2])  # Predict average temperature

    return np.array(X), np.array(y), scaler

# Load the dataset

data = load_dataset("vitaliy-sharandin/climate-krakow-temp-monthly")
df = data['train'].to_pandas()
X, y, scaler = preprocess_data(df)
print(f"Shape of X: {X.shape}, Shape of y: {y.shape}")
