### Executive Summary

- **What it is**: A Chrome MV3 extension that analyzes visible images on a page and labels them as "AI-generated" or "Real" with a confidence score.
- **How it works**: The popup triggers scanning; a content script finds visible images and draws badges; the background service worker calls a local Flask server which talks to the Hugging Face Inference API, then returns results to overlay on the page. If the API is unavailable, a deterministic mock provides a graceful fallback.
- **Why it matters**: Demonstrates a production-ready integration pattern between browser UX and ML inference, with a strong emphasis on reliability, performance, and developer experience.

#### Key Capabilities
- One-click analysis of visible images
- Overlays with labels and confidence
- Pluggable inference: external API or built-in mock
- Options page for endpoint and key configuration

#### Architecture (at a glance)
- Popup: triggers analysis
- Background SW: orchestrates, calls ML API
- Content Script: discovers images, renders overlays
- Options: stores `apiUrl`/`apiKey` in `chrome.storage.sync`
  - Local server: `simple_ai_detector.py` at `http://localhost:5001`

#### ML Approach (brief)
- Binary classifier (AI vs Real)
- CNN-based vision backbone, optionally combined with statistical/texture features
- Flask API wraps inference with a simple JSON contract
  - Current default uses zero-shot CLIP with downscaling and retry for reliability

#### Interview Talking Points
- Clean MV3 message-passing architecture (popup → background → content)
- Fault-tolerant API integration with mock fallback
- Ethical considerations, limitations, and roadmap for better accuracy
- Strong documentation and DX: clear API spec, demo script, FAQs

#### Demo Flow (60–90 seconds)
1. Load extension in dev mode
2. Open a page with images (e.g., news site)
3. Click extension → "Analyze visible images"
4. Watch badges appear with results
5. Open Settings → paste `http://localhost:5001/classify` to switch to real API
