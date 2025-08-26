#!/usr/bin/env python3
"""
Simple AI Detection API using Hugging Face
This version uses a more reliable approach for AI detection
"""

import requests
import json
from flask import Flask, request, jsonify, make_response
import os
from PIL import Image
import io
import base64
import re
import time
from collections import OrderedDict

app = Flask(__name__)

# --- CORS helpers ---
ALLOWED_ORIGINS = "*"
ALLOWED_HEADERS = "Content-Type, Authorization"
ALLOWED_METHODS = "GET, POST, OPTIONS"

def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS
    resp.headers["Access-Control-Allow-Headers"] = ALLOWED_HEADERS
    resp.headers["Access-Control-Allow-Methods"] = ALLOWED_METHODS
    return resp

@app.after_request
def apply_cors(response):
    return add_cors(response)

@app.route('/classify', methods=['OPTIONS'])
@app.route('/health', methods=['OPTIONS'])
@app.route('/', methods=['OPTIONS'])
def cors_preflight():
    return add_cors(make_response("", 204))


def _resize_and_encode_jpeg(image_bytes: bytes, max_dim: int = 512, quality: int = 85) -> str:
    """Downscale to max_dim and return base64 JPEG data URI string."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        img = img.convert('RGB')
        img.thumbnail((max_dim, max_dim), Image.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded}"


# Simple in-memory cache for recent results
_RESULT_CACHE: OrderedDict[str, dict] = OrderedDict()
_CACHE_MAX_SIZE = 500


def _cache_get(key: str):
    if key in _RESULT_CACHE:
        _RESULT_CACHE.move_to_end(key)
        return _RESULT_CACHE[key]
    return None


def _cache_set(key: str, value: dict):
    _RESULT_CACHE[key] = value
    _RESULT_CACHE.move_to_end(key)
    while len(_RESULT_CACHE) > _CACHE_MAX_SIZE:
        _RESULT_CACHE.popitem(last=False)


def detect_ai_zero_shot_clip(image_url, api_key):
    """Use zero-shot image classification (CLIP) to choose between AI-generated vs photograph."""
    try:
        cached = _cache_get(image_url)
        if cached:
            return cached

        resp = requests.get(image_url, timeout=8)
        resp.raise_for_status()

        data_uri = _resize_and_encode_jpeg(resp.content, max_dim=512, quality=85)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        model_name = "openai/clip-vit-base-patch32"
        candidate_labels = [
            "AI-generated image",
            "photograph",
            "digital art",
            "3D render",
            "illustration"
        ]

        payload = {
            "inputs": data_uri,
            "parameters": {
                "candidate_labels": candidate_labels
            }
        }

        # Retry/backoff for transient upstream errors
        for attempt in range(3):
            api_response = requests.post(
                f"https://api-inference.huggingface.co/models/{model_name}",
                json=payload,
                headers=headers,
                timeout=18
            )
            if api_response.status_code in (200, 400, 401, 403, 404):
                break
            if api_response.status_code in (502, 503, 504):
                time.sleep(0.5 * (attempt + 1))
                continue
            break

        if api_response.status_code != 200:
            return {"error": f"API error: {api_response.status_code}", "details": api_response.text}

        result = api_response.json()
        # Expected: list of {label, score}
        if isinstance(result, list) and result and isinstance(result[0], dict):
            scores = {item.get('label', ''): float(item.get('score', 0)) for item in result}
            ai_score = max(
                scores.get("AI-generated image", 0.0),
                scores.get("digital art", 0.0),
                scores.get("3D render", 0.0),
                scores.get("illustration", 0.0)
            )
            photo_score = scores.get("photograph", 0.0)

            if ai_score >= max(0.55, photo_score + 0.1):
                label = "ai"
                confidence = min(0.95, max(0.6, ai_score))
            else:
                label = "real"
                confidence = min(0.95, max(0.55, photo_score))

            out = {
                "label": label,
                "confidence": confidence,
                "source": "hf_zero_shot_clip",
                "analysis": "Zero-shot labels: " + ", ".join(f"{k}:{scores.get(k,0):.2f}" for k in ["AI-generated image","digital art","3D render","illustration","photograph"]) 
            }
            _cache_set(image_url, out)
            return out

        # Fallback
        return {"label": "real", "confidence": 0.5, "source": "hf_zero_shot_clip", "analysis": "Fallback"}
    except Exception as e:
        return {"error": str(e)}


def warmup_model(api_key):
    """Warm up Hugging Face model to reduce cold-start latency."""
    try:
        dummy_data = base64.b64encode(b"warmup").decode("utf-8")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        model_name = "google/vit-base-patch16-224"
        payload = {"inputs": f"data:image/jpeg;base64,{dummy_data}"}
        # Fire-and-forget warmup with short timeout
        requests.post(
            f"https://api-inference.huggingface.co/models/{model_name}",
            json=payload,
            headers=headers,
            timeout=3
        )
    except Exception:
        pass

@app.route('/classify', methods=['POST'])
def classify_image():
    """Flask endpoint for image classification"""
    try:
        data = request.get_json()
        image_url = data.get('imageUrl')
        api_key = os.getenv('HF_API_KEY')
        
        if not image_url:
            return add_cors(jsonify({"error": "imageUrl required"})), 400
            
        if not api_key:
            return add_cors(jsonify({"error": "HF_API_KEY environment variable required"})), 500
            
        result = detect_ai_zero_shot_clip(image_url, api_key)
        # If upstream model errored, surface a non-200 so the extension falls back cleanly
        if isinstance(result, dict) and result.get('error'):
            return add_cors(jsonify(result)), 502
        return add_cors(jsonify(result))
        
    except Exception as e:
        return add_cors(jsonify({"error": str(e)})), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    api_key = os.getenv('HF_API_KEY')
    return add_cors(jsonify({
        "status": "healthy", 
        "api_key_configured": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0
    }))

if __name__ == '__main__':
    print("Starting Simple AI Detection API...")
    print("Make sure to set HF_API_KEY environment variable")
    print("API will be available at http://localhost:5001/classify")
    # Best-effort warmup
    if os.getenv('HF_API_KEY'):
        warmup_model(os.getenv('HF_API_KEY'))
    app.run(debug=True, port=5001, host='0.0.0.0')
