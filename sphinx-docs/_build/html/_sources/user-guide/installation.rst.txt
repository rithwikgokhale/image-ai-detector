Installation Guide
==================

This guide will walk you through installing the Image AI Detector Chrome extension and setting up the API server.

System Requirements
-------------------

**Chrome Extension:**
- Google Chrome 88+ (Manifest V3 support)
- Modern browser with developer mode access

**API Server:**
- Python 3.9 or higher
- Internet connection for Hugging Face API
- 4GB+ RAM recommended

Quick Installation
------------------

.. tabs::

   .. tab:: macOS

      .. code-block:: bash

         # 1. Clone the repository
         git clone https://github.com/rithwikgokhale/image-ai-detector.git
         cd image-ai-detector

         # 2. Set up Python environment
         python3 -m venv .venv
         source .venv/bin/activate

         # 3. Install dependencies
         pip install -r requirements.txt

         # 4. Get Hugging Face API key
         # Visit: https://huggingface.co/settings/tokens
         export HF_API_KEY="hf_your_token_here"

         # 5. Start the API server
         python3 simple_ai_detector.py

   .. tab:: Windows

      .. code-block:: batch

         REM 1. Clone the repository
         git clone https://github.com/rithwikgokhale/image-ai-detector.git
         cd image-ai-detector

         REM 2. Set up Python environment
         python -m venv .venv
         .venv\Scripts\activate

         REM 3. Install dependencies
         pip install -r requirements.txt

         REM 4. Set API key (PowerShell)
         $env:HF_API_KEY="hf_your_token_here"

         REM 5. Start the API server
         python simple_ai_detector.py

   .. tab:: Linux

      .. code-block:: bash

         # 1. Clone the repository
         git clone https://github.com/rithwikgokhale/image-ai-detector.git
         cd image-ai-detector

         # 2. Set up Python environment
         python3 -m venv .venv
         source .venv/bin/activate

         # 3. Install dependencies
         pip install -r requirements.txt

         # 4. Set environment variable
         export HF_API_KEY="hf_your_token_here"

         # 5. Start the API server
         python3 simple_ai_detector.py

Chrome Extension Setup
----------------------

1. **Enable Developer Mode**

   - Open Chrome and navigate to ``chrome://extensions/``
   - Toggle "Developer mode" in the top right corner

   .. image:: ../_static/images/chrome-developer-mode.png
      :alt: Chrome Developer Mode
      :width: 600px

2. **Load the Extension**

   - Click "Load unpacked"
   - Select the ``image-ai-detector`` folder you cloned
   - The extension should appear in your extensions list

   .. image:: ../_static/images/load-unpacked.png
      :alt: Load Unpacked Extension
      :width: 600px

3. **Pin the Extension**

   - Click the extensions icon (puzzle piece) in the Chrome toolbar
   - Pin the "Image AI Detector" extension for easy access

4. **Configure API Settings**

   - Click the extension icon
   - Click "Settings"
   - Set API URL to: ``http://localhost:5001/classify``
   - Click "Test API" to verify connection

   .. image:: ../_static/images/extension-settings.png
      :alt: Extension Settings
      :width: 400px

Hugging Face API Key
--------------------

Getting Your API Key
~~~~~~~~~~~~~~~~~~~~~

1. **Create Account**

   Visit `Hugging Face <https://huggingface.co/>`_ and create a free account.

2. **Generate Token**

   - Go to `Settings → Access Tokens <https://huggingface.co/settings/tokens>`_
   - Click "New token"
   - Choose "Read" permissions
   - Copy your token (starts with ``hf_``)

3. **Set Environment Variable**

   .. tabs::

      .. tab:: macOS/Linux

         .. code-block:: bash

            # Temporary (current session)
            export HF_API_KEY="hf_your_token_here"

            # Permanent (add to ~/.bashrc or ~/.zshrc)
            echo 'export HF_API_KEY="hf_your_token_here"' >> ~/.bashrc
            source ~/.bashrc

      .. tab:: Windows

         .. code-block:: batch

            # Command Prompt
            set HF_API_KEY=hf_your_token_here

            # PowerShell
            $env:HF_API_KEY="hf_your_token_here"

            # Permanent (System Properties → Environment Variables)

.. admonition:: Free Tier Limits
   :class: note

   Hugging Face free tier provides ~1,000 API calls per month. For higher usage, consider upgrading to Pro tier or implementing local model inference.

Verification
------------

Testing the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Check API Server**

   .. code-block:: bash

      curl http://localhost:5001/health

   Expected response:

   .. code-block:: json

      {
        "status": "healthy",
        "api_key_configured": true,
        "api_key_length": 37
      }

2. **Test Classification**

   .. code-block:: bash

      curl -X POST http://localhost:5001/classify \
        -H "Content-Type: application/json" \
        -d '{"imageUrl": "https://picsum.photos/600/400"}'

   Expected response:

   .. code-block:: json

      {
        "label": "real",
        "confidence": 0.82,
        "source": "hf_zero_shot_clip",
        "analysis": "Zero-shot labels: AI-generated image:0.18, digital art:0.12, ..."
      }

3. **Test Chrome Extension**

   - Navigate to any webpage with images
   - Click the extension icon
   - Click "Analyze visible images"
   - Verify badges appear over images

Common Installation Issues
--------------------------

Python Environment Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Python Not Found

      **Error:** ``python3: command not found``

      **Solution:**

      .. code-block:: bash

         # macOS - Install via Homebrew
         brew install python3

         # Ubuntu/Debian
         sudo apt update && sudo apt install python3 python3-pip python3-venv

         # Windows - Download from python.org

   .. tab:: Permission Errors

      **Error:** ``Permission denied`` when installing packages

      **Solution:**

      .. code-block:: bash

         # Use virtual environment (recommended)
         python3 -m venv .venv
         source .venv/bin/activate
         pip install -r requirements.txt

         # Or install for user only
         pip install --user -r requirements.txt

   .. tab:: Module Import Errors

      **Error:** ``ModuleNotFoundError: No module named 'flask'``

      **Solution:**

      .. code-block:: bash

         # Ensure virtual environment is activated
         source .venv/bin/activate

         # Reinstall dependencies
         pip install -r requirements.txt

         # Check Python path
         which python
         which pip

Chrome Extension Issues
~~~~~~~~~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Extension Won't Load

      **Error:** "Failed to load extension"

      **Solutions:**
      - Ensure you selected the correct folder (containing ``manifest.json``)
      - Check Chrome version (requires 88+)
      - Look for syntax errors in console

   .. tab:: API Connection Failed

      **Error:** "Failed to fetch" in extension console

      **Solutions:**
      - Verify API server is running (``curl http://localhost:5001/health``)
      - Check firewall settings
      - Ensure API URL is correct in extension settings

   .. tab:: No Images Analyzed

      **Issue:** Extension runs but no badges appear

      **Solutions:**
      - Check if images are visible in viewport
      - Verify images are at least 32×32 pixels
      - Look for JavaScript errors in browser console

API Key Issues
~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Invalid API Key

      **Error:** ``"error": "HF_API_KEY environment variable required"``

      **Solutions:**
      - Verify environment variable is set: ``echo $HF_API_KEY``
      - Restart terminal/command prompt after setting
      - Check for typos in API key

   .. tab:: Rate Limiting

      **Error:** ``"error": "API error: 503"``

      **Solutions:**
      - Wait a few minutes and try again
      - Check Hugging Face usage limits
      - Extension will automatically fall back to mock classifier

Advanced Installation
---------------------

Docker Installation
~~~~~~~~~~~~~~~~~~~

For containerized deployment:

.. code-block:: dockerfile

   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   EXPOSE 5001

   CMD ["python", "simple_ai_detector.py"]

.. code-block:: bash

   # Build and run
   docker build -t image-ai-detector .
   docker run -p 5001:5001 -e HF_API_KEY="your_key" image-ai-detector

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For contributing to the project:

.. code-block:: bash

   # Clone with development dependencies
   git clone https://github.com/rithwikgokhale/image-ai-detector.git
   cd image-ai-detector

   # Install development dependencies
   pip install -r requirements-ml.txt

   # Install pre-commit hooks
   pre-commit install

   # Run tests
   python -m pytest tests/

Production Deployment
~~~~~~~~~~~~~~~~~~~~~

For production use with HTTPS and process management:

.. code-block:: bash

   # Install production server
   pip install gunicorn

   # Run with Gunicorn
   gunicorn --bind 0.0.0.0:5001 --workers 4 simple_ai_detector:app

   # With HTTPS (requires SSL certificates)
   gunicorn --bind 0.0.0.0:5001 --workers 4 \
     --keyfile private.key --certfile certificate.crt \
     simple_ai_detector:app

Next Steps
----------

After successful installation:

1. **Read the User Guide**: :doc:`quick-start` for basic usage
2. **Explore API Reference**: :doc:`../technical/api-reference` for integration
3. **Check Troubleshooting**: :doc:`troubleshooting` for common issues
4. **Join Development**: :doc:`../development/contributing` to contribute

.. admonition:: Need Help?
   :class: tip

   - Check the :doc:`troubleshooting` guide for common issues
   - Review :doc:`../resources/faq` for frequently asked questions
   - Open an issue on `GitHub <https://github.com/rithwikgokhale/image-ai-detector/issues>`_
