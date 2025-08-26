System Architecture
==================

The Image AI Detector follows a modern Chrome Extension MV3 architecture with clean separation of concerns and robust message passing between components.

**System Overview:**

.. code-block:: text

   User → Popup UI → Background Service Worker ← → Hugging Face API
                           ↓                              ↓
                    Content Script                   CLIP Model
                           ↓
                   Web Page Images

Core Components
---------------

Popup Interface
~~~~~~~~~~~~~~~

**File**: ``popup.html`` / ``popup.js``

The popup provides a minimal, user-friendly interface for triggering image analysis.

.. code-block:: javascript

   // Trigger analysis on active tab
   document.getElementById('analyze').addEventListener('click', () => {
     chrome.runtime.sendMessage({ type: 'ANALYZE_ACTIVE_TAB' });
     window.close();
   });

**Key Features:**
- Single-click analysis trigger
- Settings page access
- Automatic popup closure after action

Background Service Worker
~~~~~~~~~~~~~~~~~~~~~~~~~

**File**: ``background.js``

The central orchestrator that handles all API communication and message routing between components.

.. code-block:: javascript

   async function classifyImageByUrl(imageUrl) {
     const options = await chrome.storage.sync.get({ apiUrl: '', apiKey: '' });
     
     if (options.apiUrl) {
       // Call Hugging Face API with retry logic
       const response = await fetchWithTimeout(options.apiUrl, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ imageUrl })
       });
       return await response.json();
     } else {
       // Fallback to deterministic mock
       return mockClassify(imageUrl);
     }
   }

**Responsibilities:**
- API communication with Hugging Face
- Message routing between popup and content script
- Error handling and fallback logic
- Settings management via ``chrome.storage.sync``

Content Script
~~~~~~~~~~~~~~

**File**: ``content-script.js`` / ``content-style.css``

Injects into web pages to discover images and render analysis overlays.

.. code-block:: javascript

   function analyzeVisibleImages() {
     const images = Array.from(document.images).filter(isVisibleInViewport);
     
     images.forEach((img, index) => {
       const { overlay, badge } = createOverlayForImage(img);
       
       // Request classification from background
       chrome.runtime.sendMessage({
         type: 'DETECT_IMAGE_URL',
         payload: { imageUrl: img.src, requestId }
       });
     });
   }

**Key Features:**
- Intelligent image discovery (visible, minimum size)
- Real-time overlay positioning with observers
- Dynamic badge updates with confidence scores
- Cleanup on DOM mutations

Options Page
~~~~~~~~~~~~

**File**: ``options.html`` / ``options.js``

Configuration interface for API endpoints and authentication.

.. code-block:: javascript

   // Save API configuration
   await chrome.storage.sync.set({ 
     apiUrl: 'http://localhost:5001/classify',
     apiKey: 'hf_your_token_here'
   });

Data Flow Architecture
----------------------

.. tabs::

   .. tab:: User Interaction Flow

      1. **User clicks extension** → Popup opens
      2. **User clicks "Analyze"** → Popup sends ``ANALYZE_ACTIVE_TAB`` to background
      3. **Background queries active tab** → Sends ``ANALYZE_IMAGES`` to content script
      4. **Content script discovers images** → Creates overlays with "Analyzing..." badges

   .. tab:: Classification Flow

      1. **Content script finds image** → Sends ``DETECT_IMAGE_URL`` to background
      2. **Background calls API** → Hugging Face CLIP classification
      3. **API returns result** → ``{ label: 'ai'|'real', confidence: 0.87 }``
      4. **Background sends result** → ``DETECTION_RESULT`` to content script
      5. **Content script updates badge** → Shows final classification

   .. tab:: Error Handling Flow

      1. **API call fails** → Background catches error
      2. **Retry with exponential backoff** → Up to 3 attempts
      3. **Still failing?** → Fall back to deterministic mock
      4. **Always return result** → User experience never breaks

Message Passing Protocol
------------------------

The extension uses Chrome's message passing API for communication between components:

.. list-table:: Message Types
   :header-rows: 1
   :widths: 30 20 50

   * - Message Type
     - Direction
     - Purpose
   * - ``ANALYZE_ACTIVE_TAB``
     - Popup → Background
     - Trigger analysis on current tab
   * - ``ANALYZE_IMAGES``
     - Background → Content
     - Start image discovery and overlay creation
   * - ``DETECT_IMAGE_URL``
     - Content → Background
     - Request classification for specific image
   * - ``DETECTION_RESULT``
     - Background → Content
     - Return classification result with confidence

Reliability & Performance
-------------------------

Three-Tier Fallback System
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: Production Reliability
   :class: tip

   The system ensures users always get results through a carefully designed fallback hierarchy:

1. **Primary**: Hugging Face CLIP API with retry logic
2. **Secondary**: Exponential backoff for transient failures (502, 503, 504)
3. **Tertiary**: Deterministic mock classifier based on URL hash

API Resilience
~~~~~~~~~~~~~~

.. code-block:: javascript

   // Retry logic with exponential backoff
   for (let attempt = 0; attempt < 3; attempt++) {
     try {
       const response = await fetchWithTimeout(apiUrl, options, 18000);
       if (response.ok) return await response.json();
       
       if ([502, 503, 504].includes(response.status)) {
         await sleep(500 * (attempt + 1)); // Exponential backoff
         continue;
       }
       break; // Permanent error, don't retry
     } catch (error) {
       if (attempt === 2) throw error; // Last attempt
       await sleep(500 * (attempt + 1));
     }
   }

Performance Optimizations
~~~~~~~~~~~~~~~~~~~~~~~~~

**Timeout Management**
   - Image download: 8 seconds
   - API inference: 18 seconds
   - UI never blocks on network calls

**Efficient Image Discovery**
   - Only analyzes visible images (viewport intersection)
   - Minimum size filter (32×32 pixels)
   - Debounced scroll/resize handlers

**Real-time Overlay Updates**
   - ``ResizeObserver`` for image size changes
   - ``MutationObserver`` for DOM cleanup
   - Inline styles for maximum compatibility

Security Considerations
-----------------------

**Content Security Policy**
   - MV3 compliance with service workers
   - No ``eval()`` or inline scripts
   - Secure message passing between contexts

**API Key Management**
   - Stored in ``chrome.storage.sync`` (encrypted by Chrome)
   - Never exposed in content scripts
   - Optional authentication for external APIs

**Privacy Protection**
   - Images processed server-side temporarily
   - No persistent storage of image data
   - User consent through extension installation

Extensibility
-------------

The architecture supports easy extension and customization:

**Custom ML Backends**
   - Swap API endpoints via options page
   - Standard JSON request/response format
   - Pluggable authentication schemes

**Additional Image Sources**
   - Background images via computed styles
   - Canvas elements and SVGs
   - Dynamic content from JavaScript frameworks

**Enhanced Analysis**
   - Batch processing for multiple images
   - Confidence threshold configuration
   - Custom overlay styling and positioning
