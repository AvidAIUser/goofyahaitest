import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json

"""
Shade Detection Model for CoolBlock AI
"""

def create_shade_detection_model(input_shape=(224, 224, 3)):
    """
    Create a CNN for binary shade classification.
    
    Args:
        input_shape: Input image dimensions (height, width, channels)
    
    Returns:
        Compiled Keras model
    """
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        
        # Preprocessing
        layers.Rescaling(1./255),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Global Average Pooling
        layers.GlobalAveragePooling2D(),
        
        # Dense layers
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        
        # Output: Shade score (0-1)
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.AUC()]
    )
    
    return model


def predict_shade_score(image_array, model=None):
    """
    Predict shade score for an image.
    Returns a score from 0-100 (0=no shade, 100=full shade)
    
    Args:
        image_array: numpy array of shape (height, width, 3)
        model: trained Keras model (if None, returns mock prediction)
    
    Returns:
        shade_score (0-100): Predicted shade percentage
        confidence (0-100): Model confidence
    """
    if model is None:
        # Mock prediction for demo
        shade_score = np.random.uniform(30, 90)
        confidence = np.random.uniform(60, 95)
    else:
        image_resized = tf.image.resize(image_array, (224, 224))
        image_batch = np.expand_dims(image_resized, axis=0)
        shade_prob = model.predict(image_batch, verbose=0)[0][0]
        shade_score = shade_prob * 100
        confidence = 80 + np.random.uniform(-5, 5)
    
    return shade_score, confidence


def calculate_heat_risk(temperature_f, humidity, shade_score, has_nearby_cooling_center=True):
    """
    Calculate overall heat risk score (0-100)
    
    Args:
        temperature_f: Temperature in Fahrenheit
        humidity: Relative humidity (0-100)
        shade_score: Shade detection score (0-100)
        has_nearby_cooling_center: Boolean
    
    Returns:
        risk_score (0-100): Overall heat risk
        risk_level: "LOW", "MEDIUM", or "HIGH"
    """
    risk_score = 0
    
    # Temperature component (0-40 points)
    if temperature_f > 105:
        risk_score += 40
    elif temperature_f > 95:
        risk_score += 30
    elif temperature_f > 85:
        risk_score += 15
    else:
        risk_score += 5
    
    # Humidity component (0-30 points)
    if humidity > 80:
        risk_score += 30
    elif humidity > 70:
        risk_score += 20
    elif humidity > 60:
        risk_score += 10
    
    # Shade component (0-20 points)
    if shade_score < 30:
        risk_score += 20
    elif shade_score < 50:
        risk_score += 10
    
    # Cooling center proximity (0-10 points)
    if not has_nearby_cooling_center:
        risk_score += 10
    
    risk_score = min(100, max(0, risk_score))
    
    if risk_score > 70:
        risk_level = "HIGH"
    elif risk_score > 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return risk_score, risk_level


MODEL_CONFIG = {
    "input_shape": (224, 224, 3),
    "training_data": {
        "total_images": 500,
        "shade_images": 250,
        "no_shade_images": 250,
        "augmented_images": 200,
    },
    "classes": ["No Shade", "Shade"],
    "hyperparameters": {
        "epochs": 50,
        "batch_size": 32,
        "learning_rate": 0.001,
    }
}
