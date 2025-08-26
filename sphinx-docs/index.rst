Image AI Detector Documentation
================================

.. image:: https://img.shields.io/github/stars/rithwikgokhale/image-ai-detector?style=social
   :target: https://github.com/rithwikgokhale/image-ai-detector
   :alt: GitHub Stars

.. image:: https://img.shields.io/github/license/rithwikgokhale/image-ai-detector
   :target: https://github.com/rithwikgokhale/image-ai-detector/blob/main/LICENSE
   :alt: License

.. image:: https://img.shields.io/badge/Python-3.9+-blue.svg
   :target: https://python.org
   :alt: Python Version

A Chrome extension that detects AI-generated images using state-of-the-art computer vision models via Hugging Face.

.. note::
   This project uses **CLIP (Contrastive Language-Image Pretraining)** with Vision Transformers for zero-shot image classification, providing semantic understanding that generalizes across diverse AI generators.

🚀 Quick Start
--------------

.. tabs::

   .. tab:: Chrome Extension

      1. **Load the Extension**

         .. code-block:: bash

            # Clone the repository
            git clone https://github.com/rithwikgokhale/image-ai-detector.git
            cd image-ai-detector

         - Open ``chrome://extensions/`` in Chrome
         - Enable "Developer mode"
         - Click "Load unpacked" and select the project folder

      2. **Start the API Server**

         .. code-block:: bash

            # Install dependencies
            python3 -m venv .venv
            source .venv/bin/activate
            pip install -r requirements.txt

            # Set your Hugging Face API key
            export HF_API_KEY="hf_your_token_here"

            # Start the server
            python3 simple_ai_detector.py

      3. **Configure & Use**

         - Click the extension → Settings
         - Set API URL to ``http://localhost:5001/classify``
         - Visit any page with images
         - Click "Analyze visible images"

   .. tab:: API Only

      .. code-block:: bash

         # Install and run just the API
         pip install -r requirements.txt
         export HF_API_KEY="hf_your_token_here"
         python3 simple_ai_detector.py

      .. code-block:: python

         # Test the API
         import requests

         response = requests.post(
             "http://localhost:5001/classify",
             json={"imageUrl": "https://example.com/image.jpg"}
         )
         print(response.json())

✨ Features
-----------

🧠 **Advanced AI Detection**
   Uses OpenAI's CLIP model with Vision Transformers for semantic understanding

🔄 **Zero-Shot Classification**
   No training data required - works with any AI generator out of the box

⚡ **Real-Time Analysis**
   Instant overlay badges on webpage images with confidence scores

🛡️ **Production Ready**
   Fault-tolerant API with retry logic, caching, and graceful fallbacks

🎨 **Modern UI**
   Clean Chrome MV3 extension with responsive overlays

📊 **Comprehensive Analysis**
   Detailed confidence scores and reasoning for each classification

.. toctree::
   :maxdepth: 2
   :caption: Overview
   :hidden:

   executive-summary
   about-project

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   user-guide/installation
   user-guide/quick-start
   user-guide/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Technical Documentation
   :hidden:

   technical/architecture
   technical/ml-approach
   technical/api-reference

.. toctree::
   :maxdepth: 2
   :caption: Development
   :hidden:

   development/contributing

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources
   :hidden:

   resources/faq
   resources/roadmap

🎯 What Makes This Special
--------------------------

**State-of-the-Art Computer Vision**
   This project leverages CLIP's multimodal understanding, trained on 400M image-text pairs, providing semantic classification that goes beyond pixel-level analysis.

**Production Engineering**
   Built with reliability in mind - three-tier fallback system, LRU caching, exponential backoff, and conservative confidence calibration.

**Developer Experience**
   Comprehensive documentation, clean API design, and extensible architecture make it easy to integrate and customize.

.. admonition:: Why CLIP for AI Detection?
   :class: tip

   Traditional CNN classifiers require labeled training data and often overfit to specific generators. CLIP's semantic understanding, trained through contrastive learning on internet-scale data, generalizes across diverse AI generators without retraining.

🔗 Quick Links
--------------

- `GitHub Repository <https://github.com/rithwikgokhale/image-ai-detector>`_
- :doc:`technical/architecture` - System design and components
- :doc:`technical/ml-approach` - Computer vision and CLIP details
- :doc:`technical/api-reference` - Complete API documentation
- :doc:`user-guide/troubleshooting` - Common issues and solutions

**Quick Navigation:**

- 📊 :doc:`executive-summary` - Business overview and technical architecture
- ℹ️ :doc:`about-project` - Project overview for non-technical users
- 🏗️ :doc:`technical/architecture` - Chrome extension components and system design
- 🧠 :doc:`technical/ml-approach` - CLIP, Vision Transformers, and zero-shot classification  
- 🚀 :doc:`technical/api-reference` - Complete API documentation with examples
- 💡 :doc:`development/contributing` - Guidelines for contributing code and documentation