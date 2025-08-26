API Reference
=============

Complete API documentation for the Image AI Detector service.

Base URL
--------

.. code-block:: text

   http://localhost:5001

Authentication
--------------

The API requires a Hugging Face API key set as an environment variable:

.. code-block:: bash

   export HF_API_KEY="hf_your_token_here"

Get your free API key at `Hugging Face Settings <https://huggingface.co/settings/tokens>`_.

Endpoints
---------

Classify Image
~~~~~~~~~~~~~~

Classify an image as AI-generated or real using CLIP zero-shot classification.

**POST /classify**

Analyze an image URL and return classification results.

**Request:**

.. code-block:: http

   POST /classify HTTP/1.1
   Host: localhost:5001
   Content-Type: application/json

   {
     "imageUrl": "https://example.com/image.jpg"
   }

   **Response:**

   .. tabs::

      .. tab:: Success (200)

         .. code-block:: json

            {
              "label": "ai",
              "confidence": 0.87,
              "source": "hf_zero_shot_clip",
              "analysis": "Zero-shot labels: AI-generated image:0.87, digital art:0.23, 3D render:0.12, illustration:0.08, photograph:0.13"
            }

      .. tab:: Client Error (400)

         .. code-block:: json

            {
              "error": "imageUrl is required"
            }

      .. tab:: Server Error (500)

         .. code-block:: json

            {
              "error": "HF_API_KEY environment variable required"
            }

      .. tab:: Upstream Error (502)

         .. code-block:: json

            {
              "error": "API error: 503",
              "details": "Model loading"
            }

   :json string imageUrl: URL of the image to analyze (required)
   :json string label: Classification result - ``"ai"`` or ``"real"``
   :json number confidence: Confidence score between 0 and 1
   :json string source: Model identifier (``"hf_zero_shot_clip"``)
   :json string analysis: Detailed breakdown of classification scores

Health Check
~~~~~~~~~~~~

Check API status and configuration.

**GET /health**

Check API status and configuration.

**Response:**

.. code-block:: json

   {
     "status": "healthy",
     "api_key_configured": true,
     "api_key_length": 37
   }

**Response Fields:**
- ``status`` (string): Always "healthy" if service is running
- ``api_key_configured`` (boolean): Whether HF_API_KEY is set  
- ``api_key_length`` (number): Length of configured API key

Request/Response Examples
-------------------------

cURL Examples
~~~~~~~~~~~~~

.. tabs::

   .. tab:: Basic Classification

      .. code-block:: bash

         curl -X POST http://localhost:5001/classify \
           -H "Content-Type: application/json" \
           -d '{
             "imageUrl": "https://picsum.photos/600/400"
           }'

   .. tab:: Health Check

      .. code-block:: bash

         curl http://localhost:5001/health

   .. tab:: Error Handling

      .. code-block:: bash

         # Missing imageUrl
         curl -X POST http://localhost:5001/classify \
           -H "Content-Type: application/json" \
           -d '{}'

         # Response: {"error": "imageUrl is required"}

Python Examples
~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Basic Usage

      .. code-block:: python

         import requests

         def classify_image(image_url):
             response = requests.post(
                 "http://localhost:5001/classify",
                 json={"imageUrl": image_url}
             )
             
             if response.status_code == 200:
                 result = response.json()
                 print(f"Label: {result['label']}")
                 print(f"Confidence: {result['confidence']:.2f}")
                 return result
             else:
                 print(f"Error: {response.json()}")
                 return None

         # Example usage
         result = classify_image("https://example.com/image.jpg")

   .. tab:: Error Handling

      .. code-block:: python

         import requests
         from requests.exceptions import RequestException

         def robust_classify(image_url, max_retries=3):
             for attempt in range(max_retries):
                 try:
                     response = requests.post(
                         "http://localhost:5001/classify",
                         json={"imageUrl": image_url},
                         timeout=30
                     )
                     
                     if response.status_code == 200:
                         return response.json()
                     elif response.status_code == 502:
                         # Upstream error - retry
                         time.sleep(2 ** attempt)
                         continue
                     else:
                         # Client error - don't retry
                         return {"error": response.json()}
                         
                 except RequestException as e:
                     if attempt == max_retries - 1:
                         return {"error": str(e)}
                     time.sleep(2 ** attempt)
             
             return {"error": "Max retries exceeded"}

   .. tab:: Batch Processing

      .. code-block:: python

         import asyncio
         import aiohttp

         async def classify_batch(image_urls):
             """
             Classify multiple images concurrently
             """
             async def classify_single(session, url):
                 try:
                     async with session.post(
                         "http://localhost:5001/classify",
                         json={"imageUrl": url}
                     ) as response:
                         result = await response.json()
                         return {"url": url, "result": result}
                 except Exception as e:
                     return {"url": url, "error": str(e)}
             
             async with aiohttp.ClientSession() as session:
                 tasks = [classify_single(session, url) for url in image_urls]
                 results = await asyncio.gather(*tasks)
                 return results

         # Example usage
         urls = [
             "https://example.com/image1.jpg",
             "https://example.com/image2.jpg",
             "https://example.com/image3.jpg"
         ]
         results = asyncio.run(classify_batch(urls))

JavaScript Examples
~~~~~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Fetch API

      .. code-block:: javascript

         async function classifyImage(imageUrl) {
           try {
             const response = await fetch('http://localhost:5001/classify', {
               method: 'POST',
               headers: {
                 'Content-Type': 'application/json',
               },
               body: JSON.stringify({ imageUrl })
             });

             if (response.ok) {
               const result = await response.json();
               console.log(`Label: ${result.label}`);
               console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
               return result;
             } else {
               const error = await response.json();
               console.error('Classification error:', error);
               return null;
             }
           } catch (error) {
             console.error('Network error:', error);
             return null;
           }
         }

         // Example usage
         classifyImage('https://example.com/image.jpg');

   .. tab:: Chrome Extension

      .. code-block:: javascript

         // Background script
         chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
           if (message.type === 'CLASSIFY_IMAGE') {
             classifyImage(message.imageUrl)
               .then(result => sendResponse({ success: true, result }))
               .catch(error => sendResponse({ success: false, error: error.message }));
             return true; // Keep message channel open
           }
         });

         async function classifyImage(imageUrl) {
           const response = await fetch('http://localhost:5001/classify', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({ imageUrl })
           });
           
           if (!response.ok) {
             throw new Error(`HTTP ${response.status}: ${await response.text()}`);
           }
           
           return await response.json();
         }

Error Codes
-----------

.. list-table:: HTTP Status Codes
   :header-rows: 1
   :widths: 10 20 70

   * - Code
     - Meaning
     - Description
   * - 200
     - OK
     - Classification completed successfully
   * - 400
     - Bad Request
     - Invalid request format or missing imageUrl
   * - 500
     - Internal Server Error
     - Server configuration error (missing API key)
   * - 502
     - Bad Gateway
     - Upstream Hugging Face API error (model loading, rate limits)

Common Error Scenarios
~~~~~~~~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Missing API Key

      **Request:**

      .. code-block:: bash

         # HF_API_KEY not set
         curl -X POST http://localhost:5001/classify \
           -H "Content-Type: application/json" \
           -d '{"imageUrl": "https://example.com/image.jpg"}'

      **Response:**

      .. code-block:: json

         {
           "error": "HF_API_KEY environment variable required"
         }

   .. tab:: Invalid Image URL

      **Request:**

      .. code-block:: bash

         curl -X POST http://localhost:5001/classify \
           -H "Content-Type: application/json" \
           -d '{"imageUrl": "not-a-valid-url"}'

      **Response:**

      .. code-block:: json

         {
           "error": "Failed to download image: Invalid URL"
         }

   .. tab:: Model Loading

      **Request:**

      .. code-block:: bash

         # First request to cold model
         curl -X POST http://localhost:5001/classify \
           -H "Content-Type: application/json" \
           -d '{"imageUrl": "https://example.com/image.jpg"}'

      **Response:**

      .. code-block:: json

         {
           "error": "API error: 503",
           "details": "Model openai/clip-vit-base-patch32 is currently loading"
         }

Rate Limits
-----------

The API inherits rate limits from Hugging Face Inference API:

.. admonition:: Hugging Face Rate Limits
   :class: warning

   - **Free Tier**: ~1,000 requests per month
   - **Pro Tier**: Higher limits with paid subscription
   - **Rate Limit Headers**: Check response headers for current usage

   When rate limited, you'll receive a ``502`` status code. The extension automatically falls back to the deterministic mock classifier.

Model Details
-------------

Primary Model
~~~~~~~~~~~~~

.. list-table:: CLIP Model Specifications
   :header-rows: 1
   :widths: 30 70

   * - Property
     - Value
   * - Model Name
     - ``openai/clip-vit-base-patch32``
   * - Architecture
     - Vision Transformer + Text Transformer
   * - Input Size
     - 224×224 RGB images
   * - Patch Size
     - 32×32 pixels
   * - Parameters
     - ~151M parameters
   * - Training Data
     - 400M image-text pairs
   * - Inference Time
     - ~2-5 seconds (including network)

Candidate Labels
~~~~~~~~~~~~~~~~

The zero-shot classification uses these semantic labels:

.. code-block:: python

   CANDIDATE_LABELS = [
       "AI-generated image",    # Direct AI detection
       "photograph",           # Real photo baseline
       "digital art",          # Artistic AI content
       "3D render",           # Computer graphics
       "illustration"         # Hand-drawn artwork
   ]

Classification Logic
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def aggregate_scores(clip_scores):
       """
       Intelligent score aggregation for final classification
       """
       ai_indicators = [
           "AI-generated image",
           "digital art", 
           "3D render",
           "illustration"
       ]
       
       ai_score = max(clip_scores[label] for label in ai_indicators)
       photo_score = clip_scores["photograph"]
       
       # Decision boundary with margin
       if ai_score >= max(0.55, photo_score + 0.1):
           return "ai", min(0.95, max(0.6, ai_score))
       else:
           return "real", min(0.95, max(0.55, photo_score))

Performance Characteristics
---------------------------

Latency Breakdown
~~~~~~~~~~~~~~~~~

.. list-table:: Typical Response Times
   :header-rows: 1
   :widths: 40 30 30

   * - Operation
     - Typical (ms)
     - Maximum (ms)
   * - Image Download
     - 500-2000
     - 8000
   * - Image Preprocessing
     - 50-200
     - 500
   * - CLIP Inference
     - 1000-3000
     - 18000
   * - Response Processing
     - 10-50
     - 100
   * - **Total End-to-End**
     - **1500-5000**
     - **26000**

Caching Behavior
~~~~~~~~~~~~~~~~

The API implements LRU caching to improve performance:

- **Cache Size**: 500 entries
- **Cache Key**: Image URL
- **Cache Duration**: Until server restart
- **Hit Rate**: ~60-80% for typical browsing patterns

.. code-block:: python

   # Cache implementation
   from collections import OrderedDict

   _RESULT_CACHE = OrderedDict()  # LRU cache
   _CACHE_MAX_SIZE = 500

   def get_cached_result(image_url):
       if image_url in _RESULT_CACHE:
           # Move to end (most recently used)
           _RESULT_CACHE.move_to_end(image_url)
           return _RESULT_CACHE[image_url]
       return None

Monitoring and Observability
-----------------------------

Health Metrics
~~~~~~~~~~~~~~

The ``/health`` endpoint provides operational insights:

.. code-block:: json

   {
     "status": "healthy",
     "api_key_configured": true,
     "api_key_length": 37,
     "cache_size": 127,
     "cache_hit_rate": 0.73,
     "uptime_seconds": 3600,
     "requests_processed": 1543
   }

Logging
~~~~~~~

The API logs important events for debugging and monitoring:

.. code-block:: python

   import logging

   # Configure structured logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   logger = logging.getLogger(__name__)

   # Example log messages
   logger.info(f"Processing image: {image_url[:50]}...")
   logger.warning(f"API retry attempt {attempt} for upstream error {status}")
   logger.error(f"Classification failed: {error}")

Integration Examples
--------------------

Chrome Extension Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The API is designed to work seamlessly with the Chrome extension:

.. code-block:: javascript

   // Extension background script
   async function classifyImageByUrl(imageUrl) {
     const options = await chrome.storage.sync.get({ 
       apiUrl: 'http://localhost:5001/classify',
       apiKey: '' 
     });
     
     try {
       const response = await fetch(options.apiUrl, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ imageUrl })
       });
       
       if (response.ok) {
         return await response.json();
       } else {
         throw new Error(`API ${response.status}`);
       }
     } catch (error) {
       console.warn('API failed, using fallback:', error);
       return mockClassify(imageUrl);
     }
   }

Web Application Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

   <!DOCTYPE html>
   <html>
   <head>
       <title>Image AI Detector Web App</title>
   </head>
   <body>
       <input type="url" id="imageUrl" placeholder="Enter image URL">
       <button onclick="analyzeImage()">Analyze</button>
       <div id="result"></div>

       <script>
           async function analyzeImage() {
               const imageUrl = document.getElementById('imageUrl').value;
               const resultDiv = document.getElementById('result');
               
               try {
                   resultDiv.innerHTML = 'Analyzing...';
                   
                   const response = await fetch('http://localhost:5001/classify', {
                       method: 'POST',
                       headers: { 'Content-Type': 'application/json' },
                       body: JSON.stringify({ imageUrl })
                   });
                   
                   const result = await response.json();
                   
                   if (response.ok) {
                       resultDiv.innerHTML = `
                           <h3>Result: ${result.label.toUpperCase()}</h3>
                           <p>Confidence: ${(result.confidence * 100).toFixed(1)}%</p>
                           <p>Analysis: ${result.analysis}</p>
                       `;
                   } else {
                       resultDiv.innerHTML = `<p>Error: ${result.error}</p>`;
                   }
               } catch (error) {
                   resultDiv.innerHTML = `<p>Network error: ${error.message}</p>`;
               }
           }
       </script>
   </body>
   </html>
