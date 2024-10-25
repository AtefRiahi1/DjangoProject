import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
import joblib

# Chemin du fichier CSV
file_path = r'C:\Users\user\Desktop\DjangoProject\Projet_django\dashboard\recommandation\data\results.csv'

# Charger le fichier CSV
data = pd.read_csv(file_path)

# Afficher les colonnes du DataFrame
print("Colonnes du DataFrame :", data.columns.tolist())

# Vérifier le contenu du DataFrame
print(data.head())

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

    # Meilleurs paramètres trouvés par GridSearchCV
    best_params = grid_search.best_params_
    print(f"Meilleurs paramètres : {best_params}")

    # Créer et entraîner le modèle avec les meilleurs paramètres trouvés
    model = RandomForestClassifier(**best_params, random_state=42)
    model.fit(X_train, y_train)

# Prédire sur l'ensemble de test
y_pred = model.predict(X_test)

# Rapport de classification
print("Rapport de classification :")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_, labels=np.unique(y_pred)))

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
new_samples = pd.DataFrame({
    'Crop_Type': crop_encoder.transform(["blé", "maïs", "tomate"]),  # Assurez-vous que cela correspond à une catégorie existante
    'Region': region_encoder.transform(["Tunis", "Ariana", "Ben Arous", "Manouba", "Nabeul", "Zaghouan", 
        "Bizerte", "Béja", "Jendouba", "Le Kef", "Siliana", "Sousse", 
        "Monastir", "Mahdia", "Kairouan", "Kasserine", "Sidi Bouzid", 
        "Gabès", "Médenine", "Tataouine", "Gafsa", "Tozeur", "Kebili","Sfax"]),  # Assurez-vous que cela correspond à une catégorie existante
    'Average_Temperature_C': [20, 18, 22],
    'Total_Precipitation': [24, 30, 18]
})

# Vérifiez le DataFrame avant la prédiction
print("DataFrame avant la prédiction :")
print(new_samples)

# Faire des prédictions
predictions = model.predict(new_samples)

# Les étiquettes inversées
predictions_labels = label_encoder.inverse_transform(predictions)

print("Prédictions :", predictions_labels)
