### Setup & Demo

#### 1) Load the Chrome Extension (Dev Mode)
- Open `chrome://extensions/`
- Enable Developer mode
- Click "Load unpacked" → select project folder
- Pin the extension icon

#### 2) Run the Local Server (for real inference)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export HF_API_KEY="<your_hugging_face_token>"
python3 simple_ai_detector.py
# API: http://localhost:5001/classify
```

#### 3) Configure the Extension API
- Click extension → Settings
- API URL: `http://localhost:5001/classify`
- (Optional) API Key: paste if your server requires it

#### 4) Demo Script (60–90s)
1. Open a news/photo site with multiple images
2. Click the extension → "Analyze visible images"
3. Badges show up with labels and confidences
4. Open Settings → point to your API → analyze again

#### 5) Troubleshooting
- No badges? Ensure the page has visible images ≥ 32×32
- Mixed content/CORS? Serve API over HTTPS in production
- Popup closes instantly? That’s intended after triggering analysis
- Check console: background/service worker logs and network calls
 - If a badge shows “Timed out,” re-run; first request can be slower due to model warm-up
