import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from .utils.lstm_model import LSTMModel
from utils.data_loader import load_huggingface_data
from utils.data_preprocessing import preprocess_data

# Load data
data = load_huggingface_data()
X, y, scaler = preprocess_data(data[['temperature', 'humidity']].values)

# Convert data to PyTorch tensors
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32)

# Initialize the model
model = LSTMModel(input_size=2, hidden_size=64, num_layers=2, output_size=2)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()

    output = model(X_tensor)
    loss = criterion(output, y_tensor)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Save the trained model
torch.save(model.state_dict(), 'lstm_model.pth')
print("Model saved successfully.")
