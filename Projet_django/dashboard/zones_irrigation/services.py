import os
import numpy as np
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from transformers import AutoImageProcessor, AutoModelForImageClassification, pipeline


class WaterNeedsPredictor:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(BASE_DIR, 'model.h5')

        # Chargement du modèle si le fichier existe
        if os.path.isfile(self.model_path):
            self.model = load_model(self.model_path)
            print("Modèle chargé avec succès.")
        else:
            print("Erreur : Le modèle n'a pas été trouvé. Veuillez vérifier le chemin du modèle.")
            self.model = None  # S'assurer que self.model est défini même si le fichier n'existe pas

        # Initialiser le modèle Hugging Face pour la classification d'images
        self.image_classifier = pipeline("image-classification", model="jazzmacedo/fruits-and-vegetables-detector-36")
        self.processor = AutoImageProcessor.from_pretrained("jazzmacedo/fruits-and-vegetables-detector-36")
        self.model_auto = AutoModelForImageClassification.from_pretrained("jazzmacedo/fruits-and-vegetables-detector-36")

    def preprocess_image(self, image_path):
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        return np.expand_dims(img_array, axis=0)

    @staticmethod
    def create_model():
        input_layer = Input(shape=(224, 224, 3))
        x = Conv2D(32, (3, 3), activation='relu')(input_layer)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Conv2D(64, (3, 3), activation='relu')(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Flatten()(x)
        x = Dense(128, activation='relu')(x)
        output_class = Dense(len(WaterNeedsPredictor.get_class_names()), activation='softmax')(x)
        output_regression = Dense(1)(x)  # Pour la régression
        
        model = Model(inputs=input_layer, outputs=[output_class, output_regression])
        model.compile(optimizer='adam', loss=['categorical_crossentropy', 'mse'], metrics=['accuracy'])
        return model

    @staticmethod
    def get_class_names():
        return [
            "apple", "banana", "orange", "grape", "strawberry", "blueberry", 
            "raspberry", "blackberry", "kiwi", "pineapple", "mango", "peach", 
            "plum", "pear", "cherry", "apricot", "cantaloupe", "honeydew", "grapes",
            "watermelon", "papaya", "pomegranate", "lime", "lemon", "coconut",
            "fig", "date", "passionfruit", "tangerine", "nectarine", "persimmon",
            "jackfruit", "dragonfruit", "custard apple", "starfruit", "guava",
            "carrot", "beetroot", "tomato", "cucumber", "pepper", "onion", 
            "garlic", "potato", "sweet potato", "spinach", "kale", "lettuce", 
            "cabbage", "broccoli", "cauliflower", "zucchini", "eggplant", 
            "radish", "asparagus", "artichoke", "celery", "mushroom", 
            "turnip", "parsnip", "brussels sprouts", "green bean", "pea", 
            "pumpkin", "squash", "bok choy", "arugula", "swiss chard"
        ]

    def classify_image(self, image_path, confidence_threshold=0.9):
        classification_results = self.image_classifier(image_path)
        labels_and_scores = [(result['label'], result['score']) for result in classification_results]

        fruits_et_legumes = self.get_class_names()
        detected_fruits_and_vegetables = [
            (label, score) for label, score in labels_and_scores 
            if label in fruits_et_legumes and score >= confidence_threshold
        ]

        if detected_fruits_and_vegetables:
            print(f"Type(s) détecté(s) avec score(s) : {detected_fruits_and_vegetables}")
            return detected_fruits_and_vegetables
        else:
            print("Aucun fruit ou légume détecté.")
            return []

    def is_fruit_or_vegetable(self, image_path):
        resultats = self.classify_image(image_path)

        if resultats:
            print(f"Fruits ou légumes détectés: {resultats}")
            return resultats  # Retourner les résultats détectés
        else:
            print("Aucun fruit ou légume détecté.")
            return []
        
    def predict(self, image_path, superficie):
        if self.model is None:
            raise ValueError("Le modèle n'est pas chargé. Assurez-vous que le fichier model.h5 existe.")

        # Step 1: Use `is_fruit_or_vegetable` to verify if a fruit or vegetable is detected in the image
        fruits_or_vegetables = self.is_fruit_or_vegetable(image_path)

        # If no fruit or vegetable is detected, return None
        if not fruits_or_vegetables:
            print(f"Aucun fruit ou légume détecté dans l'image.")
            return None, None

        # Get the first detected result (fruit or vegetable label)
        label, score = fruits_or_vegetables[0]
        
        # Find the class index based on the label (name of the detected fruit or vegetable)
        class_index = self.get_class_names().index(label)

        # Step 2: Preprocess the image
        img_data = self.preprocess_image(image_path)

        # Step 3: Make the prediction using the model
        predictions = self.model.predict(img_data)  # Input the image data for prediction

        # Get the water need prediction
        water_need_prediction = round(predictions[1][0][0] * superficie * 10, 2)  # Assuming the second output is for water needs

        # Return the detected label and calculated water need
        print(f"Label: {label}, Water Need Prediction: {water_need_prediction}")
        return label, water_need_prediction




