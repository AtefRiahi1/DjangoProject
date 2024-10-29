import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
import joblib

file_path = r'C:\Users\user\Desktop\DjangoProject\Projet_django\dashboard\recommandation\data\results.csv'

data = pd.read_csv(file_path)

print("Colonnes du DataFrame :", data.columns.tolist())

print(data.head())

print("Longueurs des colonnes :")
for col in data.columns:
    print(f"{col}: {len(data[col])}")

data.dropna(inplace=True)

# Vérifier les longueurs des colonnes après suppression des valeurs manquantes
print("Longueurs des colonnes après suppression des valeurs manquantes :")
for col in data.columns:
    print(f"{col}: {len(data[col])}")

# Encoder les labels pour la colonne 'recommendation'
label_encoder = LabelEncoder()
data['recommendation'] = label_encoder.fit_transform(data['recommendation'])

# Encoder les colonnes catégorielles 'Crop_Type' et 'Region'
crop_encoder = LabelEncoder()
region_encoder = LabelEncoder()

data['Crop_Type'] = crop_encoder.fit_transform(data['Crop_Type'])
data['Region'] = region_encoder.fit_transform(data['Region'])

# Sauvegarder les encodeurs
joblib.dump(crop_encoder, r'C:\Users\user\Desktop\DjangoProject\Projet_django\dashboard\recommandation\data\crop_encoder.pkl')
joblib.dump(region_encoder, r'C:\Users\user\Desktop\DjangoProject\Projet_django\dashboard\recommandation\data\region_encoder.pkl')

# Séparer les caractéristiques et la cible
X = data[['Crop_Type', 'Region', 'Average_Temperature_C', 'Total_Precipitation']]
y = data['recommendation']

# Rééchantillonnage pour équilibrer les classes
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)

# Séparer le jeu de données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Afficher la distribution des classes dans l'ensemble d'entraînement
class_counts = np.bincount(y_train)
print("Distribution des classes dans l'ensemble d'entraînement :", class_counts)

# Vérifiez que vous avez assez d'échantillons dans chaque classe
min_class_size = np.min(class_counts)

# Ajustez le nombre de splits pour GridSearchCV
if min_class_size < 2:
    print("Trop peu d'échantillons pour effectuer la validation croisée. Utilisation de l'ensemble d'entraînement entier.")
    # Entraîner sans validation croisée
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
else:
    cv_splits = min(5, min_class_size)  # Ne pas dépasser 5 splits
    cv = StratifiedKFold(n_splits=cv_splits)

    # Utiliser GridSearchCV pour trouver les meilleurs hyperparamètres pour le modèle RandomForestClassifier
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_features': ['auto', 'sqrt', 'log2'],
        'max_depth': [4, 6, 8, 10],
        'criterion': ['gini', 'entropy']
    }

    # Lancer GridSearchCV
    grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42), param_grid=param_grid, cv=cv, n_jobs=-1)

    # Entraînement
    try:
        grid_search.fit(X_train, y_train)
    except ValueError as e:
        print(f"Erreur pendant l'ajustement : {e}")
        exit()

    # Meilleurs paramètres trouvés par GridSearchCV
    best_params = grid_search.best_params_
    print(f"Meilleurs paramètres : {best_params}")

    # Créer et entraîner le modèle avec les meilleurs paramètres trouvés
    model = RandomForestClassifier(**best_params, random_state=42)
    model.fit(X_train, y_train)

# Prédire sur l'ensemble de test
y_pred = model.predict(X_test)

# Obtenez les classes uniques présentes dans y_train et y_test
unique_classes_train = np.unique(y_train)
unique_classes_test = np.unique(y_test)

# Rapport de classification
print("Rapport de classification :")
print(classification_report(y_test, y_pred, target_names=label_encoder.inverse_transform(unique_classes_test), labels=unique_classes_test))

# Sauvegarder le modèle entraîné
model_path = r'C:\Users\user\Desktop\DjangoProject\Projet_django\dashboard\recommandation\data\irrigation_model.pkl'
joblib.dump(model, model_path)

print(f"Modèle entraîné sauvegardé sous {model_path}")

# -----------------------------------------------
# Section pour charger le modèle et faire des prédictions
# -----------------------------------------------

# Charger le modèle et les encodeurs
model = joblib.load(model_path)
crop_encoder = joblib.load(r'C:\Users\user\Desktop\DjangoProject\Projet_django\dashboard\recommandation\data\crop_encoder.pkl')
region_encoder = joblib.load(r'C:\Users\user\Desktop\DjangoProject\Projet_django\dashboard\recommandation\data\region_encoder.pkl')

# Préparer de nouveaux échantillons pour la prédiction
# Préparer de nouveaux échantillons pour la prédiction
new_samples_data = {
    'Crop_Type': ["blé", "maïs", "tomate", "Coffe", "poivron", "haricot", 
                  "patate", "pois", "carotte", "betterave", "pomme de terre", 
                  "ail", "raisin", "pêche", "olives", "citrons", "figues", 
                  "dattes", "menthe", "grenades", "melon", "raisin", 
                  "Aubergine", "Mangue"],
    'Region': ["Tunis", "Ariana", "Ben Arous", "Manouba", "Nabeul", 
               "Zaghouan", "Bizerte", "Béja", "Jendouba", "Le Kef", 
               "Siliana", "Sousse", "Monastir", "Mahdia", "Kairouan", 
               "Kasserine", "Sidi Bouzid", "Gabès", "Médenine", 
               "Tataouine", "Gafsa", "Tozeur", "Kebili", "Sfax"],
    'Average_Temperature_C': [18.0, 27.0, 30.0, 25.0, 28.0, 22.0, 24.0, 21.0,
                              23.0, 25.0, 26.0, 20.0, 30.0, 22.0, 32.0, 28.0,
                              26.0, 34.0, 24.0, 35.0, 36.0, 36.0, 30.0, 28.0],
    'Total_Precipitation': [100.0, 200.0, 150.0, 120.0, 200.0, 50.0, 90.0, 150.0, 70.0, 100.0,
                            80.0, 60.0, 150.0, 120.0, 40.0, 200.0, 70.0, 50.0, 30.0, 40.0,
                            20.0, 20.0, 150.0, 200.0]
}

# Harmoniser la longueur des colonnes
max_length = max(len(v) for v in new_samples_data.values())
for key, values in new_samples_data.items():
    if len(values) < max_length:
        new_samples_data[key] += [None] * (max_length - len(values))

# Convertir en DataFrame
new_samples = pd.DataFrame(new_samples_data)

# Supprimer les lignes avec des valeurs manquantes
new_samples.dropna(inplace=True)

# Encoder les nouvelles données
new_samples['Crop_Type'] = crop_encoder.transform(new_samples['Crop_Type'])
new_samples['Region'] = region_encoder.transform(new_samples['Region'])

# Faire des prédictions sur les nouveaux échantillons
predictions = model.predict(new_samples)

# Décoder les prédictions
decoded_predictions = label_encoder.inverse_transform(predictions)

# Afficher les recommandations
for crop, region, pred in zip(new_samples['Crop_Type'], new_samples['Region'], decoded_predictions):
    print(f"Recommandation pour {crop_encoder.inverse_transform([crop])[0]} dans la région {region_encoder.inverse_transform([region])[0]} : {pred}")
