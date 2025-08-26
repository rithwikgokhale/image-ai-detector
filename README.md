# Image AI Detector (Chrome Extension)

Label the images you see on any webpage as “AI-generated” or “Real,” with a confidence score.

This project includes a Chrome extension and a small local server that calls the Hugging Face Inference API. It is designed to be easy to run for non-technical users and easy to extend for developers.

## Quick Links
- Executive Summary: `docs/Executive-Summary.md`
- Non‑technical Guide: `docs/Guide-For-Non-Technical-Users.md`
- Setup & Demo: `docs/Setup-and-Demo.md`
- Architecture: `docs/Architecture.md`
- API Spec (Hugging Face CLIP): `docs/API-Spec.md`
- ML Approach (Computer Vision): `docs/ML-Approach.md`
- FAQ: `docs/FAQ.md`
- Roadmap: `docs/Roadmap.md`

## What It Does
- One‑click analysis from the popup
- Finds visible images and overlays badges with a label and confidence
- Pluggable backend: a local Flask server that talks to Hugging Face
- Graceful timeouts so overlays don’t “hang” if the network is slow

## How It Works (at a glance)
- You click the extension → it scans visible images on the page
- For each image, the extension asks the local server to classify it
- The server downloads the image and sends it to a Hugging Face model
- The extension overlays the result as a small badge on the image

## Quickstart (macOS)
1) Install Python 3.9+.
2) Run the local server:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export HF_API_KEY="<your_hugging_face_token>"
python3 simple_ai_detector.py
# Server runs at http://localhost:5001
```
3) Load the extension:
- Open `chrome://extensions/` → enable Developer mode → Load unpacked → choose this folder
- Click the extension, then “Settings,” and set the API URL to:
  `http://localhost:5001/classify`
4) Visit any page with images and click “Analyze visible images.”

Troubleshooting? See `docs/FAQ.md` and the “Troubleshooting” section in `docs/Setup-and-Demo.md`.

## Requirements
- Extension: modern Chrome (Manifest V3)
- Local server: Python 3.9+, `pip install -r requirements.txt`
- Hugging Face token: create one in your HF account and set `HF_API_KEY`

## Repo Structure
```
ML Chrome Extension/
  manifest.json
  background.js
  content-script.js
  content-style.css
  popup.html
  popup.js
  options.html
  options.js
  simple_ai_detector.py      # Local Flask server (default)
  test_api.py                # Quick health/classify tests
  requirements.txt           # Minimal deps for the local server
  requirements-ml.txt        # Optional deps for example ML training server
  ml_model_example.py        # Example ML server (optional/demo)
  train_model.py             # Example training script (optional/demo)
  docs/
```

## Contributing
See `CONTRIBUTING.md` for guidelines. Issues and pull requests are welcome.

## License
MIT – see `LICENSE`.
