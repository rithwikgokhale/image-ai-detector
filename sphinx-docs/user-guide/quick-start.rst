Quick Start Guide
=================

Get up and running with Image AI Detector in under 5 minutes.

Prerequisites
-------------

- Chrome browser with developer mode
- Python 3.9+ installed
- Internet connection

Step 1: Get the Code
--------------------

.. code-block:: bash

   git clone https://github.com/rithwikgokhale/image-ai-detector.git
   cd image-ai-detector

Step 2: Set Up API Server
--------------------------

.. code-block:: bash

   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Get free API key from https://huggingface.co/settings/tokens
   export HF_API_KEY="hf_your_token_here"

   # Start server
   python3 simple_ai_detector.py

You should see:

.. code-block:: text

   Starting Simple AI Detection API...
   Make sure to set HF_API_KEY environment variable
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5001
   * Running on http://localhost:5001

Step 3: Install Chrome Extension
---------------------------------

1. Open ``chrome://extensions/`` in Chrome
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the ``image-ai-detector`` folder
5. Pin the extension to your toolbar

Step 4: Configure Extension
----------------------------

1. Click the extension icon
2. Click "Settings"
3. Set API URL to: ``http://localhost:5001/classify``
4. Click "Test API" - should show success message

Step 5: Try It Out!
--------------------

1. Navigate to any webpage with images (try a news site)
2. Click the extension icon
3. Click "Analyze visible images"
4. Watch badges appear over images with classifications!

.. admonition:: First Analysis Tips
   :class: tip

   - The first API call may take 10-15 seconds (model loading)
   - Subsequent calls are much faster (~2-5 seconds)
   - Extension falls back to mock classifier if API fails

Example Results
---------------

You'll see badges like these over images:

.. list-table:: Badge Examples
   :header-rows: 1
   :widths: 30 70

   * - Badge
     - Meaning
   * - 🟢 **Real • 89%**
     - High confidence this is a real photograph
   * - 🟣 **AI-generated • 76%**
     - High confidence this is AI-generated
   * - 🟡 **Real • 52%**
     - Low confidence, uncertain classification

What's Happening Under the Hood?
---------------------------------

1. **Extension scans page** for visible images ≥32×32 pixels
2. **Sends image URLs** to your local API server
3. **Server downloads images** and sends to Hugging Face CLIP model
4. **CLIP analyzes semantically** using labels like "AI-generated image" vs "photograph"
5. **Results returned** with confidence scores and displayed as overlays

Next Steps
----------

**Explore Advanced Features:**
- :doc:`../technical/ml-approach` - Learn about the CLIP model
- :doc:`../technical/api-reference` - Integrate with your own applications
- :doc:`../development/extending` - Customize the extension

**Troubleshooting:**
- :doc:`troubleshooting` - Common issues and solutions
- :doc:`../resources/faq` - Frequently asked questions

**Get Involved:**
- :doc:`../development/contributing` - Contribute to the project
- `GitHub Issues <https://github.com/rithwikgokhale/image-ai-detector/issues>`_ - Report bugs or request features
