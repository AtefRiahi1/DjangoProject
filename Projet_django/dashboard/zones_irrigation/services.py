from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten ,Conv2D, MaxPooling2D
import numpy as np

# Exemple de données
X_train = np.random.rand(100, 224, 224, 3)  # 100 images 224x224 RGB
y_train = np.random.rand(100)  # Valeurs cibles aléatoires

# Création d'un modèle simple
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='linear')
])


# Compilation du modèle
model.compile(optimizer='adam', loss='mean_squared_error')

# Entraînement du modèle
model.fit(X_train, y_train, epochs=5)



# Enregistrez-le au format Keras
model.save('SMAP_L4_SM_aup_20230121T000000_Vv7030_001.h5')

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Chemin vers le répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Spécifiez le chemin vers le modèle
model_path = os.path.join(BASE_DIR, 'SMAP_L4_SM_aup_20230121T000000_Vv7030_001.h5')

# Vérifiez si le fichier existe
if os.path.isfile(model_path):
    model = load_model(model_path)
else:
    raise FileNotFoundError(f"Le fichier n'existe pas : {model_path}")

def predict_water_need(image_path, superficie):
    # Prétraiter l'image
    img = load_img(image_path, target_size=(224, 224))  # Charger et redimensionner l'image
    img_array = img_to_array(img) / 255.0  # Normaliser les pixels entre 0 et 1
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter une dimension pour le batch

    # Prédire le besoin en eau
    prediction = model.predict(img_array)
    
    # Ajuster la prédiction par la superficie
    return prediction[0][0] * superficie