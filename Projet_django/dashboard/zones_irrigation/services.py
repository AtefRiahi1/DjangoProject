from keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os

# Création du modèle avec l'API fonctionnelle
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Input

# Input layer
input_layer = Input(shape=(224, 224, 3))

# Convolutional layers
x = Conv2D(32, (3, 3), activation='relu')(input_layer)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

# Flatten the output
x = Flatten()(x)

# Dense layers
x = Dense(128, activation='relu')(x)

# Outputs
classification_output = Dense(1, activation='sigmoid', name='classification_output')(x)
regression_output = Dense(1, activation='linear', name='regression_output')(x)

# Create the model
model = Model(inputs=input_layer, outputs=[classification_output, regression_output])

# Compilation du modèle avec deux objectifs : binaire pour la classification, et erreur quadratique pour la régression
model.compile(optimizer='adam', 
              loss={'classification_output': 'binary_crossentropy', 'regression_output': 'mean_squared_error'}, 
              metrics={'classification_output': 'accuracy'})

# Exemple de données avec étiquettes supplémentaires pour la classification binaire
y_class = np.random.randint(0, 2, size=(100,))  # 0 pour non-plante, 1 pour plante
y_reg = np.random.rand(100)  # Besoin en eau
X_train = np.random.rand(100, 224, 224, 3)  # 100 images 224x224 RGB

# Entraînement du modèle
model.fit(X_train, {'classification_output': y_class, 'regression_output': y_reg}, epochs=5)

# Enregistrement du modèle
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

    # Obtenir les deux prédictions (classification et régression)
    predictions = model.predict(img_array)

    # Les deux sorties sont dans un tableau
    is_plant = predictions[0][0]  # Sortie de la classification
    water_need = predictions[1][0] * superficie * 10 # Sortie de la régression pour le besoin en eau

    # Vérifier si l'image est une plante
    if is_plant >= 0.5:  # Si le modèle prédit que c'est une plante
        return f"Besoin en eau estimé : {water_need} litres"
    else:
        return "Ce n'est pas une plante"