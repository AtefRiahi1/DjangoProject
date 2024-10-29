# scripts/load_data.py
import pandas as pd
from ..models import Capteur, Mesure

def load_data():
    df = pd.read_csv('data.xls')

    sensor = Capteur.objects.get_or_create(
        nom_capteur="Field Sensor",
        )[0]

    for _, row in df.iterrows():
        Mesure.objects.create(
            capteur=sensor,
            temperature=row['temp'],
            moisture=row['moisture'],
            should_irrigate=row['pump']
        )
    print("Data loaded successfully.")
