import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from home.models import ConsommationEau
import os

def train_model(user):
    user_data = ConsommationEau.objects.filter(user=user).values()
    user_df = pd.DataFrame(user_data)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(BASE_DIR, 'consommationEau', 'dataset.csv')
    csv_df = pd.read_csv(model_path) 

    combined_df = pd.concat([user_df, csv_df], ignore_index=True)

    X = combined_df[['temperature', 'humidite', 'precipitations', 'type_culture', 'phase_culture']]
    y = combined_df['quantite_consommee']

    X = pd.get_dummies(X, columns=['type_culture', 'phase_culture'], drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')

    return model, X.columns.tolist()  