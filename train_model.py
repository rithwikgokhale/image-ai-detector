"""
Simplified training script for the AI Image Detection model.
This demonstrates the complete ML pipeline from data to trained model.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from PIL import Image
import requests
from io import BytesIO
import json

# Import our model functions
from ml_model_example import (
    download_and_preprocess_image,
    extract_statistical_features,
    create_cnn_model,
    create_data_generator
)

def create_sample_dataset():
    """
    Create a small sample dataset for demonstration.
    In practice, you'd use real datasets with thousands of images.
    """
    print("Creating sample dataset...")
    
    # Sample image URLs (replace with real datasets)
    # Real images from Unsplash
    real_images = [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
        "https://images.unsplash.com/photo-1518837695005-2083093ee35b",
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e"
    ]
    
    # AI-generated images (replace with actual AI-generated images)
    # For demo, we'll use some artistic images that might be AI-generated
    ai_images = [
        "https://images.unsplash.com/photo-1578662996442-48f60103fc96",  # Artistic
        "https://images.unsplash.com/photo-1541961017774-22349e4a1262",  # Abstract
        "https://images.unsplash.com/photo-1578662996442-48f60103fc96",
        "https://images.unsplash.com/photo-1541961017774-22349e4a1262",
        "https://images.unsplash.com/photo-1578662996442-48f60103fc96"
    ]
    
    return real_images, ai_images

def download_and_save_sample_images():
    """
    Download sample images and save them locally for training.
    """
    real_urls, ai_urls = create_sample_dataset()
    
    # Create directories
    os.makedirs('data/real', exist_ok=True)
    os.makedirs('data/ai', exist_ok=True)
    
    # Download real images
    for i, url in enumerate(real_urls):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            image = image.convert('RGB')
            image = image.resize((224, 224))
            
            image.save(f'data/real/real_{i}.jpg')
            print(f"Downloaded real image {i+1}/{len(real_urls)}")
            
        except Exception as e:
            print(f"Error downloading real image {i}: {e}")
    
    # Download AI images
    for i, url in enumerate(ai_urls):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            image = image.convert('RGB')
            image = image.resize((224, 224))
            
            image.save(f'data/ai/ai_{i}.jpg')
            print(f"Downloaded AI image {i+1}/{len(ai_urls)}")
            
        except Exception as e:
            print(f"Error downloading AI image {i}: {e}")

def create_local_data_generator(batch_size=2):
    """
    Create a data generator using local images.
    """
    real_dir = 'data/real'
    ai_dir = 'data/ai'
    
    real_files = [f for f in os.listdir(real_dir) if f.endswith('.jpg')]
    ai_files = [f for f in os.listdir(ai_dir) if f.endswith('.jpg')]
    
    while True:
        batch_images = []
        batch_labels = []
        
        for _ in range(batch_size):
            # Randomly choose real or AI
            if np.random.random() < 0.5 and real_files:
                # Real image
                filename = np.random.choice(real_files)
                image_path = os.path.join(real_dir, filename)
                label = 0
            elif ai_files:
                # AI image
                filename = np.random.choice(ai_files)
                image_path = os.path.join(ai_dir, filename)
                label = 1
            else:
                continue
            
            try:
                # Load and preprocess image
                image = Image.open(image_path)
                image = image.convert('RGB')
                image = image.resize((224, 224))
                image_array = np.array(image) / 255.0
                
                batch_images.append(image_array)
                batch_labels.append(label)
                
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                continue
        
        if len(batch_images) > 0:
            yield np.array(batch_images), np.array(batch_labels)

def train_simple_model():
    """
    Train a simple model with the sample data.
    """
    print("Training model...")
    
    # Create model
    model = create_cnn_model()
    
    # Create data generators
    train_generator = create_local_data_generator(batch_size=2)
    val_generator = create_local_data_generator(batch_size=2)
    
    # Training callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy',
            save_best_only=True
        )
    ]
    
    # Train model
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=10,  # Small number for demo
        steps_per_epoch=5,
        validation_steps=2,
        callbacks=callbacks,
        verbose=1
    )
    
    print("Training completed!")
    return model, history

def test_model(model):
    """
    Test the trained model on sample images.
    """
    print("\nTesting model...")
    
    # Test on a few sample images
    test_images = [
        ('data/real/real_0.jpg', 'Real'),
        ('data/ai/ai_0.jpg', 'AI')
    ]
    
    for image_path, expected in test_images:
        try:
            # Load and preprocess
            image = Image.open(image_path)
            image = image.convert('RGB')
            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0
            image_input = np.expand_dims(image_array, axis=0)
            
            # Predict
            prediction = model.predict(image_input)
            ai_probability = prediction[0][1]
            
            # Determine result
            if ai_probability > 0.5:
                result = 'AI'
                confidence = ai_probability
            else:
                result = 'Real'
                confidence = 1 - ai_probability
            
            print(f"Image: {image_path}")
            print(f"Expected: {expected}, Predicted: {result}")
            print(f"Confidence: {confidence:.2f}")
            print(f"AI Probability: {ai_probability:.2f}")
            print("-" * 40)
            
        except Exception as e:
            print(f"Error testing {image_path}: {e}")

def main():
    """
    Main training pipeline.
    """
    print("=== AI Image Detection Model Training ===")
    
    # Step 1: Download sample data
    print("\n1. Downloading sample images...")
    download_and_save_sample_images()
    
    # Step 2: Train model
    print("\n2. Training model...")
    model, history = train_simple_model()
    
    # Step 3: Test model
    print("\n3. Testing model...")
    test_model(model)
    
    # Step 4: Save model
    print("\n4. Saving model...")
    model.save('final_model.h5')
    print("Model saved as 'final_model.h5'")
    
    print("\n=== Training Complete ===")
    print("You can now use this model with the Chrome extension!")
    print("To use with the extension:")
    print("1. Start the Flask API: python ml_model_example.py")
    print("2. In the extension options, set API URL to: http://localhost:5000/classify")

if __name__ == '__main__':
    main()
