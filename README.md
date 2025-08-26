# 🤖 Image AI Detector

> **Real-time AI-generated image detection for the web** - A Chrome extension that instantly analyzes images on any webpage to distinguish between authentic photographs and AI-generated content.

[![GitHub Stars](https://img.shields.io/github/stars/rithwikgokhale/image-ai-detector?style=social)](https://github.com/rithwikgokhale/image-ai-detector)
[![License](https://img.shields.io/github/license/rithwikgokhale/image-ai-detector)](https://github.com/rithwikgokhale/image-ai-detector/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)

## 🎯 What It Does

In today's digital world, **AI-generated images** are becoming increasingly sophisticated and widespread. This Chrome extension helps you:

- 🔍 **Detect AI-generated images** on any webpage instantly
- 📊 **Get confidence scores** for each classification
- 🎨 **See visual overlays** directly on images
- 🛡️ **Make informed decisions** about content authenticity

## ✨ Key Features

- 🧠 **State-of-the-Art ML**: Uses CLIP (Contrastive Language-Image Pretraining) with Vision Transformers
- ⚡ **Real-Time Analysis**: Instant results as you browse
- 🔄 **Zero-Shot Classification**: Works with any AI generator without retraining
- 🎨 **Visual Overlays**: Clear badges and confidence scores on images
- 🛡️ **Privacy-First**: Local processing where possible, secure API communication
- 📱 **Easy to Use**: One-click activation, no technical knowledge required

## 🚀 Quick Start

### 1. Install Dependencies
```bash
git clone https://github.com/rithwikgokhale/image-ai-detector.git
cd image-ai-detector
pip install -r requirements.txt
```

### 2. Set Up API Key
```bash
export HF_API_KEY="your_hugging_face_token_here"
```

### 3. Start the Server
```bash
python3 simple_ai_detector.py
```

### 4. Load Extension
- Open `chrome://extensions/` in Chrome
- Enable "Developer mode"
- Click "Load unpacked" and select the project folder
- Visit any webpage with images and click the extension icon

## 📊 Example Results

```json
{
  "label": "ai",
  "confidence": 0.87,
  "source": "image_analysis_heuristic",
  "analysis": "Size: 800x600 (480,000px), Aspect: 1.33"
}
```

## 🏗️ Technology Stack

- **Frontend**: Chrome Extension (JavaScript, Manifest V3)
- **Backend**: Flask API (Python)
- **ML Engine**: Hugging Face Transformers
- **Image Processing**: PIL/Pillow
- **Analysis**: Computer Vision & Pattern Recognition

## 📚 Documentation

📖 **Complete documentation**: [View Documentation](https://your-netlify-site.netlify.app)

- 📊 [Executive Summary](https://your-netlify-site.netlify.app/executive-summary.html) - Business overview
- ℹ️ [About Project](https://your-netlify-site.netlify.app/about-project.html) - Non-technical guide
- 🏗️ [Technical Architecture](https://your-netlify-site.netlify.app/technical/architecture.html) - System design
- 🧠 [ML Approach](https://your-netlify-site.netlify.app/technical/ml-approach.html) - Computer vision details

## 🎯 Use Cases

- **Content Creators**: Verify image authenticity before sharing
- **Journalists**: Fact-check visual content
- **Educators**: Teach digital literacy and media awareness
- **Social Media Users**: Make informed decisions about what to share
- **Business Professionals**: Ensure marketing materials are authentic

## 🔧 API Usage

```python
import requests

response = requests.post(
    "http://localhost:5001/classify",
    json={"imageUrl": "https://example.com/image.jpg"}
)
result = response.json()
print(f"Classification: {result['label']} (Confidence: {result['confidence']:.2%})")
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for a more transparent digital world**
