#!/usr/bin/env python3
"""
Test script for the Hugging Face AI Detection API
"""

import requests
import json

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:5001/health')
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_classification():
    """Test image classification with a sample image"""
    try:
        # Use a sample image URL
        test_image_url = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4"
        
        payload = {
            "imageUrl": test_image_url
        }
        
        response = requests.post(
            'http://localhost:5001/classify',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Classification status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Classification test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Hugging Face AI Detection API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_health()
    
    # Test classification endpoint
    print("\n2. Testing classification endpoint...")
    classification_ok = test_classification()
    
    if health_ok and classification_ok:
        print("\n✅ API is working correctly!")
    else:
        print("\n❌ API has issues. Check the server logs.")
