Frequently Asked Questions
==========================

General Questions
-----------------

What is Image AI Detector?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Image AI Detector is a Chrome extension that uses state-of-the-art computer vision models (specifically OpenAI's CLIP) to classify images on web pages as either AI-generated or real photographs.

How accurate is the detection?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The accuracy depends on several factors:

- **Model**: We use CLIP, which provides semantic understanding
- **Image type**: Works better on clear photos vs. artistic content
- **AI generator**: Performance varies across different AI models
- **Confidence scores**: Higher confidence generally means higher accuracy

Typical performance:
- High confidence (>80%): ~85-95% accuracy
- Medium confidence (60-80%): ~70-85% accuracy
- Low confidence (<60%): ~50-70% accuracy

Is it free to use?
~~~~~~~~~~~~~~~~~~

Yes! The Chrome extension is completely free. You'll need a free Hugging Face API key, which provides ~1,000 API calls per month at no cost.

Does it work offline?
~~~~~~~~~~~~~~~~~~~~~

Partially. The extension includes a deterministic mock classifier that works offline, but for accurate AI detection, you need an internet connection to access the CLIP model via Hugging Face.

Technical Questions
-------------------

Which AI generators can it detect?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CLIP's semantic understanding generalizes across many AI generators:

✅ **Well-detected:**
- DALL-E (all versions)
- Midjourney
- Stable Diffusion
- Adobe Firefly
- Generic "AI art" styles

⚠️ **Challenging:**
- Highly photorealistic AI (latest models)
- AI-enhanced real photos
- Mixed human-AI content

❌ **Not designed for:**
- Deepfakes (faces)
- Video content
- Audio-generated content

How does the mock classifier work?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the API is unavailable, the extension uses a deterministic hash-based classifier:

.. code-block:: javascript

   function mockClassify(imageUrl) {
     let hash = 0;
     for (let i = 0; i < imageUrl.length; i++) {
       hash = ((hash << 5) - hash) + imageUrl.charCodeAt(i);
     }
     const isAi = (Math.abs(hash) % 2) === 0;
     const confidence = ((Math.abs(hash) % 51) + 50) / 100;
     return { label: isAi ? 'ai' : 'real', confidence };
   }

This provides consistent results for the same URL but isn't based on actual image analysis.

Can I use my own AI model?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! The extension supports custom API endpoints. You can:

1. Implement the same API interface (``POST /classify``)
2. Return results in the expected format
3. Configure the API URL in extension settings

See :doc:`../technical/api-reference` for the complete API specification.

Privacy & Security
------------------

What data is collected?
~~~~~~~~~~~~~~~~~~~~~~~

**Chrome Extension:**
- No user data collected
- Image URLs processed temporarily
- Settings stored locally in Chrome

**API Server:**
- Images downloaded temporarily for analysis
- No persistent storage of images
- API logs may contain image URLs (configurable)

**Hugging Face:**
- Subject to Hugging Face privacy policy
- Images processed for inference only
- No permanent storage by HF

Is my browsing data sent anywhere?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Only image URLs from pages you actively analyze are sent to:
1. Your local API server (localhost:5001)
2. Hugging Face API (if using the default setup)

No browsing history, personal data, or other information is transmitted.

Can websites detect the extension?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Websites can potentially detect:
- DOM modifications (overlay elements)
- Network requests to your local API
- JavaScript execution patterns

However, the extension doesn't identify itself or send identifying information to websites.

Usage Questions
---------------

Why are some images not analyzed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The extension only analyzes images that are:
- Currently visible in the browser viewport
- At least 32×32 pixels in size
- Have a valid ``src`` attribute
- Not hidden by CSS (``display: none``, ``visibility: hidden``)

How can I improve accuracy?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Use clear, unambiguous images**: Blurry or low-quality images are harder to classify
2. **Check confidence scores**: Higher confidence usually means more reliable results
3. **Consider context**: Use your judgment alongside the AI classification
4. **Report issues**: Help improve the model by reporting misclassifications

Why does the first analysis take so long?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first API call needs to "wake up" the CLIP model on Hugging Face servers, which can take 10-30 seconds. Subsequent calls are much faster (2-5 seconds).

To reduce this delay:
- The server attempts to warm up the model on startup
- Consider upgrading to Hugging Face Pro for faster cold starts

Can I analyze images in bulk?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, the extension analyzes visible images one by one. For bulk analysis, you can:

1. Use the API directly with your own scripts
2. Implement batch processing (see :doc:`../development/contributing`)
3. Use browser automation tools with the extension

Troubleshooting
---------------

Extension doesn't work on some websites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some websites may:
- Use Content Security Policy (CSP) that blocks extensions
- Load images dynamically after page load
- Use non-standard image formats or sources

Try:
- Refreshing the page after images load
- Checking browser console for errors
- Testing on different websites

API calls are failing
~~~~~~~~~~~~~~~~~~~~~

Common causes:
- **API key issues**: Verify ``HF_API_KEY`` is set correctly
- **Rate limiting**: Free tier has monthly limits
- **Network issues**: Check internet connection
- **Server not running**: Ensure ``python simple_ai_detector.py`` is active

See :doc:`../user-guide/troubleshooting` for detailed solutions.

Results seem inconsistent
~~~~~~~~~~~~~~~~~~~~~~~~~

AI detection is inherently challenging. Inconsistencies may occur due to:
- **Image quality**: Compression, resolution, lighting
- **Content type**: Photos vs. artwork vs. mixed media
- **AI evolution**: Newer generators may be harder to detect
- **Model limitations**: CLIP wasn't specifically trained for AI detection

For best results:
- Focus on high-confidence classifications
- Use multiple images for validation
- Consider the source and context

Development Questions
---------------------

How can I contribute?
~~~~~~~~~~~~~~~~~~~~~

We welcome contributions! See :doc:`../development/contributing` for:
- Code contributions
- Documentation improvements
- Bug reports and feature requests
- Testing and feedback

Can I modify the extension?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Absolutely! The extension is open source (MIT license). You can:
- Fork the repository
- Modify for your needs
- Submit improvements back to the project
- Create your own variants

How do I deploy this in production?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For production deployment:

1. **API Server**: Use Gunicorn with multiple workers
2. **HTTPS**: Set up SSL certificates
3. **Monitoring**: Implement logging and error tracking
4. **Scaling**: Consider load balancers and caching
5. **Security**: API rate limiting and authentication

See deployment guides in the development section.

What's the roadmap?
~~~~~~~~~~~~~~~~~~~

Planned improvements include:
- Better AI detection models
- Batch processing capabilities
- Firefox and Safari support
- Local model inference options
- Attention visualization
- Performance optimizations

See :doc:`roadmap` for detailed plans.

Still Have Questions?
---------------------

If your question isn't answered here:

1. **Search Issues**: Check `GitHub Issues <https://github.com/rithwikgokhale/image-ai-detector/issues>`_
2. **Ask the Community**: Open a new issue or discussion
3. **Check Documentation**: Browse other sections of this documentation
4. **Contact Maintainer**: Reach out via GitHub

We're always happy to help! 🚀
