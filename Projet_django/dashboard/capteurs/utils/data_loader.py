import pandas as pd
import requests

def load_huggingface_data():
    url = "https://huggingface.co/datasets/openclimatefix/soil_moisture_temperature/resolve/main/soil_data.csv"
    response = requests.get(url)
    with open('soil_data.csv', 'wb') as f:
        f.write(response.content)
    return pd.read_csv('soil_data.csv')

def prepare_sensor_data(capteur):
    data = capteur.mesures.all().values('temperature', 'humidity', 'date_mesure')
    return pd.DataFrame(data)
