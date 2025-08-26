Troubleshooting
===============

Common issues and their solutions.

Extension Issues
----------------

Extension Won't Load
~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
- "Failed to load extension" error
- Extension doesn't appear in Chrome

**Solutions:**

.. tabs::

   .. tab:: Check Manifest

      Ensure you selected the correct folder containing ``manifest.json``:

      .. code-block:: bash

         ls image-ai-detector/
         # Should show: manifest.json, background.js, popup.html, etc.

   .. tab:: Chrome Version

      Verify Chrome version supports Manifest V3:

      .. code-block:: text

         chrome://version/
         # Should show version 88 or higher

   .. tab:: Console Errors

      Check for errors in ``chrome://extensions/``:
      
      - Click "Errors" button next to the extension
      - Look for JavaScript syntax errors
      - Fix any reported issues

No Images Being Analyzed
~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
- Extension runs but no badges appear
- "Analyze visible images" does nothing

**Solutions:**

.. tabs::

   .. tab:: Image Visibility

      Extension only analyzes visible images:

      - Images must be in viewport (scroll to see them)
      - Minimum size: 32×32 pixels
      - Must have ``src`` attribute

   .. tab:: Console Errors

      Check browser console (F12):

      .. code-block:: javascript

         // Look for errors like:
         // "Failed to fetch"
         // "CORS error"
         // "Network error"

   .. tab:: API Connection

      Verify API server is running:

      .. code-block:: bash

         curl http://localhost:5001/health
         # Should return: {"status": "healthy", ...}

Badges Disappear on Scroll
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**
- Badges appear but vanish when scrolling
- Overlays don't follow image movement

**Solutions:**

This is usually a temporary issue. The extension uses observers to track image movement:

.. code-block:: javascript

   // Extension automatically handles:
   // - Scroll events
   // - Resize events  
   // - DOM mutations
   // - Image size changes

If persistent, try:
- Refresh the page
- Disable/re-enable the extension
- Check for JavaScript errors in console

API Server Issues
-----------------

Server Won't Start
~~~~~~~~~~~~~~~~~~

**Error:** ``ModuleNotFoundError`` or import errors

**Solutions:**

.. tabs::

   .. tab:: Virtual Environment

      Ensure virtual environment is activated:

      .. code-block:: bash

         # Check if activated (should show (.venv))
         which python
         
         # If not activated:
         source .venv/bin/activate  # macOS/Linux
         .venv\Scripts\activate     # Windows

   .. tab:: Dependencies

      Reinstall dependencies:

      .. code-block:: bash

         pip install -r requirements.txt
         
         # Verify installation
         pip list | grep -E "(flask|requests|pillow)"

   .. tab:: Python Version

      Check Python version:

      .. code-block:: bash

         python --version
         # Should be 3.9 or higher

API Key Issues
~~~~~~~~~~~~~~

**Error:** ``"HF_API_KEY environment variable required"``

**Solutions:**

.. tabs::

   .. tab:: Set Environment Variable

      .. code-block:: bash

         # Check if set
         echo $HF_API_KEY
         
         # Set if missing
         export HF_API_KEY="hf_your_token_here"
         
         # Verify
         curl http://localhost:5001/health

   .. tab:: Get Valid API Key

      1. Visit `Hugging Face Settings <https://huggingface.co/settings/tokens>`_
      2. Create new token with "Read" permissions
      3. Copy token (starts with ``hf_``)
      4. Set environment variable

   .. tab:: Persistent Storage

      Add to shell profile for persistence:

      .. code-block:: bash

         # macOS/Linux
         echo 'export HF_API_KEY="hf_your_token"' >> ~/.bashrc
         source ~/.bashrc

Model Loading Errors
~~~~~~~~~~~~~~~~~~~~~

**Error:** ``"API error: 503"`` or ``"Model loading"``

**Solutions:**

.. tabs::

   .. tab:: Wait and Retry

      Hugging Face models need time to load:

      .. code-block:: bash

         # Wait 30-60 seconds, then retry
         curl -X POST http://localhost:5001/classify \
           -H "Content-Type: application/json" \
           -d '{"imageUrl": "https://picsum.photos/600"}'

   .. tab:: Model Warmup

      The server automatically warms up models on startup, but you can manually trigger:

      .. code-block:: bash

         # Multiple quick requests help load the model
         for i in {1..3}; do
           curl -X POST http://localhost:5001/classify \
             -H "Content-Type: application/json" \
             -d '{"imageUrl": "https://picsum.photos/600"}' &
         done

   .. tab:: Check Hugging Face Status

      Visit `Hugging Face Status <https://status.huggingface.co/>`_ to check for service issues.

Network and CORS Issues
-----------------------

CORS Errors in Browser
~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``"Access to fetch at 'http://localhost:5001' from origin 'https://example.com' has been blocked by CORS policy"``

**Solution:**

The API server includes CORS headers. If you still see errors:

.. code-block:: python

   # In simple_ai_detector.py, CORS is already configured:
   @app.after_request
   def apply_cors(response):
       response.headers["Access-Control-Allow-Origin"] = "*"
       response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
       response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
       return response

Connection Refused
~~~~~~~~~~~~~~~~~~

**Error:** ``"Connection refused"`` or ``"ECONNREFUSED"``

**Solutions:**

.. tabs::

   .. tab:: Check Server Status

      .. code-block:: bash

         # Verify server is running
         ps aux | grep simple_ai_detector
         
         # Check port binding
         netstat -an | grep 5001
         lsof -i :5001

   .. tab:: Firewall Settings

      .. code-block:: bash

         # macOS - Allow Python through firewall
         # System Preferences → Security & Privacy → Firewall → Options
         # Add Python to allowed apps
         
         # Linux - Check iptables
         sudo iptables -L
         
         # Windows - Check Windows Defender Firewall

   .. tab:: Port Conflicts

      .. code-block:: bash

         # Check if port 5001 is in use
         lsof -i :5001
         
         # Use different port if needed
         python simple_ai_detector.py --port 5002

Performance Issues
------------------

Slow Response Times
~~~~~~~~~~~~~~~~~~~

**Symptoms:**
- API calls take >30 seconds
- Extension seems to hang

**Solutions:**

.. tabs::

   .. tab:: Network Optimization

      .. code-block:: python

         # Server automatically implements:
         # - Image compression (JPEG quality=85)
         # - Size limits (max 512px)
         # - Timeouts (18s for inference)
         # - Retry logic with backoff

   .. tab:: Caching

      Enable result caching:

      .. code-block:: python

         # Already implemented - LRU cache with 500 entries
         # Check cache hit rate:
         curl http://localhost:5001/health
         # Look for "cache_hit_rate" in response

   .. tab:: Hugging Face Performance

      - Free tier has lower priority
      - Consider upgrading to Pro tier for faster inference
      - Peak hours (US/EU business hours) may be slower

Memory Issues
~~~~~~~~~~~~~

**Error:** ``"Memory error"`` or system slowdown

**Solutions:**

.. tabs::

   .. tab:: Reduce Batch Size

      Analyze fewer images at once:

      .. code-block:: javascript

         // Extension automatically limits concurrent requests
         // But you can reduce image discovery:
         function isVisibleInViewport(element) {
             const rect = element.getBoundingClientRect();
             // Only analyze images in immediate viewport
             return rect.top >= 0 && rect.bottom <= window.innerHeight;
         }

   .. tab:: Clear Cache

      .. code-block:: bash

         # Restart server to clear cache
         pkill -f simple_ai_detector
         python simple_ai_detector.py

   .. tab:: System Resources

      .. code-block:: bash

         # Check memory usage
         top -p $(pgrep -f simple_ai_detector)
         
         # Close other applications if needed
         # Consider running on a machine with more RAM

Debugging Tools
---------------

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # In simple_ai_detector.py, set debug mode:
   if __name__ == '__main__':
       app.run(debug=True, port=5001, host='0.0.0.0')

Browser Developer Tools
~~~~~~~~~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: Extension Console

      .. code-block:: text

         1. Open chrome://extensions/
         2. Find "Image AI Detector"
         3. Click "background page" or "service worker"
         4. Check console for errors

   .. tab:: Page Console

      .. code-block:: text

         1. Press F12 on any webpage
         2. Go to Console tab
         3. Look for extension-related errors
         4. Check Network tab for failed API calls

   .. tab:: Extension Storage

      .. code-block:: javascript

         // Check extension settings
         chrome.storage.sync.get(null, console.log);
         
         // Clear settings if needed
         chrome.storage.sync.clear();

API Testing Tools
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Test health endpoint
   curl -v http://localhost:5001/health

   # Test classification with verbose output
   curl -v -X POST http://localhost:5001/classify \
     -H "Content-Type: application/json" \
     -d '{"imageUrl": "https://picsum.photos/600"}'

   # Check response headers
   curl -I http://localhost:5001/health

Getting Help
------------

If you're still experiencing issues:

1. **Check the FAQ**: :doc:`../resources/faq`
2. **Search existing issues**: `GitHub Issues <https://github.com/rithwikgokhale/image-ai-detector/issues>`_
3. **Create a new issue** with:
   - Operating system and version
   - Python version (``python --version``)
   - Chrome version (``chrome://version/``)
   - Complete error messages
   - Steps to reproduce

**Include Debug Information:**

.. code-block:: bash

   # System info
   python --version
   pip list
   echo $HF_API_KEY | cut -c1-10  # First 10 chars only
   
   # API server logs
   python simple_ai_detector.py 2>&1 | tee debug.log
   
   # Extension console logs (copy from browser dev tools)
