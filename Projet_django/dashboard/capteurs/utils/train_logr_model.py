import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Load the dataset
df = pd.read_csv('data.xls')

# Preprocessing: Extract features and target
X = df[['temp', 'moisture']]
y = df['pump']  # Assuming 'Irrigation' is the target column

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Test the model and print accuracy
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Save the trained model to a file
with open('irrigation_model.pkl', 'wb') as f:
    pickle.dump(model, f)
