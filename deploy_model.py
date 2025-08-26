#!/usr/bin/env python3
"""
Deploy the existing ML model as a Flask API
This uses the CNN model from ml_model_example.py
"""

import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO
import base64

# Import the model functions
from ml_model_example import (
    download_and_preprocess_image,
    extract_statistical_features,
    create_cnn_model
)

app = Flask(__name__)

# Global model variable
model = None

def load_or_create_model():
    """Load pre-trained model or create a new one"""
    global model
    
    model_path = 'trained_model.h5'
    
    if os.path.exists(model_path):
        print("Loading pre-trained model...")
        model = tf.keras.models.load_model(model_path)
    else:
        print("Creating new model (untrained)...")
        model = create_cnn_model()
        # Note: This model won't be accurate without training data
        print("WARNING: Model is untrained and will give random predictions")
    
    return model

def classify_image_with_model(image_url):
    """
    Classify image using the loaded model
    """
    try:
        # Download and preprocess image
        image_array = download_and_preprocess_image(image_url)
        
        if image_array is None:
            return {"error": "Failed to process image"}
        
        # Reshape for model input
        image_input = np.expand_dims(image_array, axis=0)
        
        # Get model prediction
        prediction = model.predict(image_input, verbose=0)
        
        # Extract results
        ai_probability = prediction[0][1]  # Assuming index 1 is AI class
        real_probability = prediction[0][0]  # Assuming index 0 is real class
        
        # Determine label and confidence
        if ai_probability > real_probability:
            label = "ai"
            confidence = float(ai_probability)
        else:
            label = "real"
            confidence = float(real_probability)
        
        return {
            "label": label,
            "confidence": confidence,
            "source": "custom_model",
            "ai_prob": float(ai_probability),
            "real_prob": float(real_probability)
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.route('/classify', methods=['POST'])
def classify_image():
    """Flask endpoint for image classification"""
    try:
        data = request.get_json()
        image_url = data.get('imageUrl')
        
        if not image_url:
            return jsonify({"error": "imageUrl required"}), 400
        
        result = classify_image_with_model(image_url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model_loaded": model is not None})

if __name__ == '__main__':
    # Load model on startup
    load_or_create_model()
    
    # Run the Flask app
    print("Starting AI Detection API on http://localhost:5000")
    print("Use POST /classify with {'imageUrl': 'url'} to classify images")
    app.run(debug=True, port=5000, host='0.0.0.0')
