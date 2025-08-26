# AI Image Detector Extension - Setup Guide

## Current Status
Your extension currently uses a **mock classifier** that randomly assigns labels. To make it work properly, you need to implement one of the options below.

## Option 1: Google AI Detection API (Recommended - Easiest)

### Setup Steps:
1. **Get Google API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

2. **Install Dependencies**:
   ```bash
   pip3 install flask requests
   ```

3. **Set Environment Variable**:
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

4. **Run the API Server**:
   ```bash
   python3 google_ai_detector.py
   ```

5. **Configure Extension**:
   - Open extension options (right-click extension icon → Options)
   - Set API URL to: `http://localhost:5000/classify`
   - Leave API Key empty (it's handled server-side)

### Pros:
- ✅ Free tier available
- ✅ High accuracy
- ✅ No training required
- ✅ Easy to set up

### Cons:
- ❌ Requires internet connection
- ❌ Rate limits on free tier

---

## Option 2: Hugging Face Models (Best Accuracy)

### Setup Steps:
1. **Get Hugging Face API Key**:
   - Go to [Hugging Face](https://huggingface.co/settings/tokens)
   - Create a new access token
   - Copy the token

2. **Install Dependencies**:
   ```bash
   pip3 install flask requests pillow
   ```

3. **Set Environment Variable**:
   ```bash
   export HF_API_KEY="your_token_here"
   ```

4. **Run the API Server**:
   ```bash
   python3 huggingface_detector.py
   ```

5. **Configure Extension**:
   - Set API URL to: `http://localhost:5000/classify`
   - Leave API Key empty

### Pros:
- ✅ State-of-the-art models
- ✅ Very high accuracy
- ✅ Multiple model options

### Cons:
- ❌ Requires internet
- ❌ May have costs for heavy usage

---

## Option 3: Deploy Your Own Model (Most Control)

### Setup Steps:
1. **Install Dependencies**:
   ```bash
   pip3 install flask tensorflow pillow requests numpy
   ```

2. **Train the Model** (Optional):
   ```bash
   python3 train_model.py
   ```
   This will create a `trained_model.h5` file

3. **Run the API Server**:
   ```bash
   python3 deploy_model.py
   ```

4. **Configure Extension**:
   - Set API URL to: `http://localhost:5000/classify`

### Pros:
- ✅ Works offline
- ✅ No API costs
- ✅ Full control

### Cons:
- ❌ Requires training data
- ❌ Lower accuracy without good training data
- ❌ More complex setup

---

## Quick Start (Recommended)

For the fastest working solution:

1. **Use Google API** (Option 1):
   ```bash
   # Install dependencies
   pip3 install flask requests
   
   # Get API key from Google AI Studio
   export GOOGLE_API_KEY="your_key"
   
   # Run server
   python3 google_ai_detector.py
   ```

2. **Configure Extension**:
   - Right-click extension icon → Options
   - API URL: `http://localhost:5000/classify`
   - API Key: (leave empty)

3. **Test**:
   - Go to any website with images
   - Click the extension icon
   - Images should now be properly classified

---

## Production Deployment

For production use, you'll want to:

1. **Deploy the API** to a cloud service (Heroku, AWS, etc.)
2. **Update the extension** to use your production API URL
3. **Add error handling** and rate limiting
4. **Monitor usage** and costs

---

## Troubleshooting

### Common Issues:
- **"API failed" errors**: Check your API key and internet connection
- **No classifications**: Ensure the API server is running
- **Slow responses**: Consider caching or using a faster model

### Testing:
- Use the `/health` endpoint to check if your API is working
- Test with known AI-generated vs real images
- Monitor accuracy on different types of content

---

## Next Steps

1. Choose an option above and set it up
2. Test the extension on various websites
3. Monitor accuracy and adjust as needed
4. Consider adding features like:
   - Confidence thresholds
   - Batch processing
   - User feedback collection
   - Model retraining pipeline
