### API Specification

#### Endpoint
- Method: `POST`
- Path: `/classify`
- Content-Type: `application/json`
- Default Port: `5001` (Hugging Face CLIP API)

#### Request Body
```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

#### Success Response (200)
```json
{
  "label": "ai",                    // "ai" | "real"
  "confidence": 0.87,               // number in [0,1]
  "source": "hf_zero_shot_clip",    // model identifier
  "analysis": "Zero-shot labels: AI-generated image:0.87, digital art:0.23, 3D render:0.12, illustration:0.08, photograph:0.13"
}
```

#### Error Responses
- `400` → invalid payload or unreachable image
```json
{ "error": "imageUrl is required" }
```
- `500` → internal error or missing API key
```json
{ "error": "HF_API_KEY environment variable required" }
```
- `502` → upstream model error (extension falls back to mock)
```json
{ "error": "API error: 503", "details": "Model loading" }
```

#### Example Setup & Usage
```bash
# 1. Get Hugging Face API key from https://huggingface.co/settings/tokens
export HF_API_KEY="hf_your_token_here"

# 2. Start the API server
python simple_ai_detector.py

# 3. Test the endpoint
curl -s -X POST http://localhost:5001/classify \
  -H 'Content-Type: application/json' \
  -d '{"imageUrl": "https://picsum.photos/600"}'
```

#### Authentication
- **Environment Variable**: `HF_API_KEY=hf_your_token_here`
- **Get API Key**: https://huggingface.co/settings/tokens (free tier available)
- **Model Used**: OpenAI CLIP-ViT-Base-Patch32 via Hugging Face Inference API

#### Health Check
```bash
curl http://localhost:5001/health
# Response: {"status": "healthy", "api_key_configured": true, "api_key_length": 37}
```

#### Model Details
- **Architecture**: Vision Transformer (ViT) with 32x32 patches
- **Approach**: Zero-shot classification with candidate labels
- **Labels**: "AI-generated image", "photograph", "digital art", "3D render", "illustration"
- **Decision Logic**: AI score vs photograph score with calibrated confidence
- **Preprocessing**: RGB conversion, Lanczos resize to 512px, JPEG optimization