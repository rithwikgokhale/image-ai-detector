### Guide for Non‑Technical Users

This guide helps you use the Image AI Detector without needing to code.

#### What this does
It adds small labels on top of pictures you see online. Each label says if the picture is likely “AI‑generated” or “Real,” and shows a confidence number.

#### Step 1: Start the helper app
1. Open the project folder
2. Double‑click Terminal (or open it from Applications → Utilities)
3. Copy and paste these commands, one line at a time:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export HF_API_KEY="<paste your Hugging Face token>"
python3 simple_ai_detector.py
```
Leave that window open. It keeps the helper app running.

#### Step 2: Add the extension to Chrome
1. In Chrome, open `chrome://extensions/`
2. Turn on “Developer mode”
3. Click “Load unpacked” and choose the project folder
4. Pin the “Image AI Detector” icon if you want

#### Step 3: Tell the extension where the helper app is
1. Click the extension icon → click “Settings”
2. Paste this into “API URL”: `http://localhost:5001/classify`
3. Click “Save” and close the page

#### Step 4: Try it out
1. Open any page with pictures
2. Click the extension → “Analyze visible images”
3. Watch as labels appear on the images

#### Tips
- First use can be slower while it “warms up”
- If an image says “Timed out,” click the extension again
- This tool is not always correct; treat results as hints


