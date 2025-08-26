"""
Practical ML Model for AI-Generated Image Detection
This example shows how to build a real classifier that could be deployed as an API.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import cv2
from PIL import Image
import requests
from io import BytesIO
import json
from flask import Flask, request, jsonify

# ============================================================================
# 1. DATA PREPARATION & FEATURE EXTRACTION
# ============================================================================

def download_and_preprocess_image(image_url, target_size=(224, 224)):
    """
    Download image from URL and preprocess for model input.
    
    Args:
        image_url (str): URL of the image
        target_size (tuple): Target size (width, height)
    
    Returns:
        np.array: Preprocessed image array
    """
    try:
        # Download image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Load image
        image = Image.open(BytesIO(response.content))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize
        image = image.resize(target_size)
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        return image_array
    
    except Exception as e:
        print(f"Error processing image {image_url}: {e}")
        return None

def extract_statistical_features(image):
    """
    Extract statistical features that help distinguish AI vs real images.
    
    Args:
        image (np.array): Image array (H, W, C)
    
    Returns:
        dict: Statistical features
    """
    # Convert to grayscale for some analyses
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    features = {}
    
    # 1. Basic statistics
    features['mean_intensity'] = np.mean(gray)
    features['std_intensity'] = np.std(gray)
    features['skewness'] = np.mean(((gray - np.mean(gray)) / np.std(gray)) ** 3)
    features['kurtosis'] = np.mean(((gray - np.mean(gray)) / np.std(gray)) ** 4)
    
    # 2. Edge density (AI images often have different edge patterns)
    edges = cv2.Canny(gray, 50, 150)
    features['edge_density'] = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # 3. Local binary pattern (texture analysis)
    features['lbp_variance'] = extract_lbp_features(gray)
    
    # 4. Color distribution
    for i, color in enumerate(['red', 'green', 'blue']):
        channel = image[:, :, i]
        features[f'{color}_mean'] = np.mean(channel)
        features[f'{color}_std'] = np.std(channel)
    
    return features

def extract_lbp_features(gray_image, radius=3, n_points=8):
    """
    Extract Local Binary Pattern features for texture analysis.
    """
    # Simplified LBP implementation
    height, width = gray_image.shape
    lbp_image = np.zeros((height, width), dtype=np.uint8)
    
    for i in range(radius, height - radius):
        for j in range(radius, width - radius):
            center = gray_image[i, j]
            binary = 0
            for k in range(n_points):
                angle = 2 * np.pi * k / n_points
                x = int(i + radius * np.cos(angle))
                y = int(j + radius * np.sin(angle))
                if gray_image[x, y] >= center:
                    binary |= (1 << k)
            lbp_image[i, j] = binary
    
    return np.var(lbp_image)

# ============================================================================
# 2. DEEP LEARNING MODEL ARCHITECTURE
# ============================================================================

def create_cnn_model(input_shape=(224, 224, 3)):
    """
    Create a CNN model for AI image detection.
    
    Args:
        input_shape (tuple): Input image shape (height, width, channels)
    
    Returns:
        tf.keras.Model: Compiled model
    """
    model = models.Sequential([
        # Input layer
        layers.Input(shape=input_shape),
        
        # Convolutional layers
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        # Global average pooling
        layers.GlobalAveragePooling2D(),
        
        # Dense layers
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        
        # Output layer (2 classes: real, ai)
        layers.Dense(2, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_ensemble_model():
    """
    Create an ensemble model combining CNN and statistical features.
    """
    # CNN branch
    cnn_input = layers.Input(shape=(224, 224, 3))
    cnn_model = create_cnn_model()
    cnn_output = cnn_model(cnn_input)
    
    # Statistical features branch
    stats_input = layers.Input(shape=(12,))  # Number of statistical features
    stats_dense = layers.Dense(64, activation='relu')(stats_input)
    stats_dropout = layers.Dropout(0.3)(stats_dense)
    stats_output = layers.Dense(2, activation='softmax')(stats_dropout)
    
    # Combine outputs
    combined = layers.Average()([cnn_output, stats_output])
    
    ensemble_model = models.Model(
        inputs=[cnn_input, stats_input],
        outputs=combined
    )
    
    ensemble_model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return ensemble_model

# ============================================================================
# 3. TRAINING PIPELINE
# ============================================================================

def create_data_generator(real_image_urls, ai_image_urls, batch_size=32):
    """
    Create a data generator for training.
    
    Args:
        real_image_urls (list): URLs of real images
        ai_image_urls (list): URLs of AI-generated images
        batch_size (int): Batch size for training
    
    Yields:
        tuple: (images, labels)
    """
    while True:
        # Sample batch
        batch_images = []
        batch_labels = []
        
        for _ in range(batch_size):
            # Randomly choose real or AI image
            if np.random.random() < 0.5:
                url = np.random.choice(real_image_urls)
                label = 0  # Real
            else:
                url = np.random.choice(ai_image_urls)
                label = 1  # AI
            
            # Download and preprocess
            image = download_and_preprocess_image(url)
            if image is not None:
                batch_images.append(image)
                batch_labels.append(label)
        
        if len(batch_images) > 0:
            yield np.array(batch_images), np.array(batch_labels)

def train_model(model, train_generator, validation_generator, epochs=50):
    """
    Train the model with callbacks and monitoring.
    """
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7
        ),
        tf.keras.callbacks.ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy',
            save_best_only=True
        )
    ]
    
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=epochs,
        callbacks=callbacks,
        steps_per_epoch=100,
        validation_steps=20
    )
    
    return history

# ============================================================================
# 4. INFERENCE & API
# ============================================================================

class AIImageDetector:
    """
    Main class for AI image detection.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the detector.
        
        Args:
            model_path (str): Path to saved model weights
        """
        self.model = create_cnn_model()
        if model_path:
            self.model.load_weights(model_path)
    
    def predict(self, image_url):
        """
        Predict whether an image is AI-generated or real.
        
        Args:
            image_url (str): URL of the image to analyze
        
        Returns:
            dict: Prediction results
        """
        # Download and preprocess image
        image = download_and_preprocess_image(image_url)
        if image is None:
            return {
                'error': 'Failed to download or process image',
                'label': 'unknown',
                'confidence': 0.0
            }
        
        # Extract statistical features
        stats_features = extract_statistical_features(image)
        
        # Prepare input for model
        image_input = np.expand_dims(image, axis=0)
        stats_input = np.array([[
            stats_features['mean_intensity'],
            stats_features['std_intensity'],
            stats_features['skewness'],
            stats_features['kurtosis'],
            stats_features['edge_density'],
            stats_features['lbp_variance'],
            stats_features['red_mean'],
            stats_features['red_std'],
            stats_features['green_mean'],
            stats_features['green_std'],
            stats_features['blue_mean'],
            stats_features['blue_std']
        ]])
        
        # Make prediction
        prediction = self.model.predict(image_input)
        ai_probability = prediction[0][1]  # Probability of being AI-generated
        
        # Determine label and confidence
        if ai_probability > 0.5:
            label = 'ai'
            confidence = ai_probability
        else:
            label = 'real'
            confidence = 1 - ai_probability
        
        return {
            'label': label,
            'confidence': float(confidence),
            'ai_probability': float(ai_probability),
            'features': stats_features
        }

# ============================================================================
# 5. FLASK API SERVER
# ============================================================================

app = Flask(__name__)
detector = AIImageDetector('best_model.h5')  # Load trained model

@app.route('/classify', methods=['POST'])
def classify_image():
    """
    API endpoint for image classification.
    
    Expected request:
    {
        "imageUrl": "https://example.com/image.jpg"
    }
    
    Response:
    {
        "label": "ai",
        "confidence": 0.87,
        "ai_probability": 0.87
    }
    """
    try:
        data = request.get_json()
        image_url = data.get('imageUrl')
        
        if not image_url:
            return jsonify({'error': 'imageUrl is required'}), 400
        
        # Make prediction
        result = detector.predict(image_url)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# ============================================================================
# 6. USAGE EXAMPLES
# ============================================================================

def example_usage():
    """
    Example of how to use the detector.
    """
    # Initialize detector
    detector = AIImageDetector()
    
    # Test images
    test_urls = [
        'https://example.com/real_image1.jpg',
        'https://example.com/ai_image1.jpg',
        'https://example.com/real_image2.jpg'
    ]
    
    # Analyze each image
    for url in test_urls:
        result = detector.predict(url)
        print(f"Image: {url}")
        print(f"Result: {result['label']} (confidence: {result['confidence']:.2f})")
        print(f"AI Probability: {result['ai_probability']:.2f}")
        print("-" * 50)

def example_training():
    """
    Example of how to train the model.
    """
    # Example URLs (you would need real datasets)
    real_image_urls = [
        'https://example.com/real1.jpg',
        'https://example.com/real2.jpg',
        # ... more real image URLs
    ]
    
    ai_image_urls = [
        'https://example.com/ai1.jpg',
        'https://example.com/ai2.jpg',
        # ... more AI image URLs
    ]
    
    # Create data generators
    train_generator = create_data_generator(
        real_image_urls[:800], 
        ai_image_urls[:800], 
        batch_size=32
    )
    
    validation_generator = create_data_generator(
        real_image_urls[800:], 
        ai_image_urls[800:], 
        batch_size=32
    )
    
    # Create and train model
    model = create_cnn_model()
    history = train_model(model, train_generator, validation_generator)
    
    # Save model
    model.save_weights('best_model.h5')
    print("Training completed!")

# ============================================================================
# 7. INTEGRATION WITH CHROME EXTENSION
# ============================================================================

def create_extension_compatible_api():
    """
    Create an API that matches the Chrome extension's expected format.
    """
    @app.route('/api/classify', methods=['POST'])
    def extension_classify():
        """
        Chrome extension compatible endpoint.
        """
        try:
            data = request.get_json()
            image_url = data.get('imageUrl')
            
            if not image_url:
                return jsonify({'error': 'imageUrl is required'}), 400
            
            # Make prediction
            result = detector.predict(image_url)
            
            if 'error' in result:
                return jsonify({'error': result['error']}), 400
            
            # Return in extension-expected format
            return jsonify({
                'label': result['label'],
                'confidence': result['confidence']
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# ============================================================================
# 8. PERFORMANCE OPTIMIZATION
# ============================================================================

def optimize_for_production():
    """
    Production optimizations for the model.
    """
    # 1. Model quantization
    converter = tf.lite.TFLiteConverter.from_keras_model(detector.model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    
    # Save optimized model
    with open('optimized_model.tflite', 'wb') as f:
        f.write(tflite_model)
    
    # 2. Batch processing
    def batch_predict(image_urls, batch_size=10):
        """Process multiple images efficiently."""
        results = []
        for i in range(0, len(image_urls), batch_size):
            batch_urls = image_urls[i:i + batch_size]
            batch_images = []
            
            for url in batch_urls:
                image = download_and_preprocess_image(url)
                if image is not None:
                    batch_images.append(image)
            
            if batch_images:
                batch_input = np.array(batch_images)
                batch_predictions = detector.model.predict(batch_input)
                
                for j, pred in enumerate(batch_predictions):
                    ai_prob = pred[1]
                    label = 'ai' if ai_prob > 0.5 else 'real'
                    confidence = ai_prob if ai_prob > 0.5 else (1 - ai_prob)
                    
                    results.append({
                        'url': batch_urls[j],
                        'label': label,
                        'confidence': float(confidence)
                    })
        
        return results

if __name__ == '__main__':
    # Run the API server
    print("Starting AI Image Detection API...")
    print("API will be available at: http://localhost:5000/classify")
    app.run(host='0.0.0.0', port=5000, debug=True)
