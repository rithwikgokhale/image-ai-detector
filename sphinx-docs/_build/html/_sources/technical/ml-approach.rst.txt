Machine Learning Approach
=========================

This project leverages state-of-the-art computer vision models to detect AI-generated images through semantic understanding rather than pixel-level analysis.

.. admonition:: Why Semantic Understanding Matters
   :class: tip

   Traditional CNN classifiers require labeled training data and often overfit to specific generators. CLIP's semantic understanding, trained through contrastive learning on internet-scale data, generalizes across diverse AI generators without retraining.

Problem Definition
------------------

**Task**: Binary classification of images as AI-generated or real

**Input**: Image URL (downloaded and preprocessed server-side)

**Output**: Structured classification result

.. code-block:: json

   {
     "label": "ai",
     "confidence": 0.87,
     "source": "hf_zero_shot_clip",
     "analysis": "Zero-shot labels: AI-generated image:0.87, digital art:0.23, ..."
   }

CLIP Architecture Deep Dive
----------------------------

OpenAI's CLIP (Contrastive Language-Image Pretraining)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use **CLIP-ViT-Base-Patch32** via Hugging Face Inference API as our primary model.

.. tabs::

   .. tab:: Vision Encoder (ViT)

      **Vision Transformer Architecture:**

      - **Input**: 224×224 RGB images
      - **Patch Size**: 32×32 pixels (196 total patches)
      - **Embedding Dimension**: 768
      - **Attention Heads**: 12
      - **Transformer Layers**: 12

      .. code-block:: python

         # Patch embedding process
         def patch_embedding(image):
             # Split 224x224 image into 14x14 grid of 32x32 patches
             patches = image.unfold(2, 32, 32).unfold(3, 32, 32)  # [196, 32, 32, 3]
             
             # Linear projection to embedding space
             embeddings = linear_projection(patches)  # [196, 768]
             
             # Add positional encoding
             pos_embeddings = positional_encoding(196)  # [196, 768]
             
             # Prepend [CLS] token
             cls_token = learnable_parameter([1, 768])
             return concat([cls_token, embeddings + pos_embeddings])  # [197, 768]

   .. tab:: Text Encoder

      **Transformer Architecture:**

      - **Context Length**: 77 tokens
      - **Vocabulary Size**: 49,408
      - **Embedding Dimension**: 768 (matches vision encoder)
      - **Attention Heads**: 12
      - **Transformer Layers**: 12

      .. code-block:: python

         # Candidate labels for zero-shot classification
         candidate_labels = [
             "AI-generated image",    # Direct AI detection
             "photograph",           # Real photo classification  
             "digital art",          # Artistic AI content
             "3D render",           # Computer graphics
             "illustration"         # Hand-drawn/digital art
         ]

   .. tab:: Multimodal Fusion

      **Contrastive Learning:**

      - **Training Data**: 400M image-text pairs from internet
      - **Loss Function**: InfoNCE (contrastive loss)
      - **Similarity**: Cosine similarity between image and text embeddings

      .. code-block:: python

         def clip_similarity(image, text_labels):
             # Encode image and text
             image_features = vision_encoder(image)      # [1, 768]
             text_features = text_encoder(text_labels)   # [5, 768]
             
             # Normalize features
             image_features = normalize(image_features)
             text_features = normalize(text_features)
             
             # Compute cosine similarity
             logits = image_features @ text_features.T   # [1, 5]
             probabilities = softmax(logits * temperature)
             
             return probabilities

Computer Vision Pipeline
------------------------

Image Preprocessing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def preprocess_image(image_bytes, max_dim=512, quality=85):
       """
       Optimized preprocessing pipeline for CLIP inference
       """
       with Image.open(io.BytesIO(image_bytes)) as img:
           # Color space normalization
           img = img.convert('RGB')
           
           # High-quality resize with Lanczos interpolation
           img.thumbnail((max_dim, max_dim), Image.LANCZOS)
           
           # JPEG optimization for API transport
           buffer = io.BytesIO()
           img.save(buffer, format='JPEG', quality=quality, optimize=True)
           
           # Base64 encoding for JSON API
           encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
           return f"data:image/jpeg;base64,{encoded}"

**Key Preprocessing Steps:**

1. **Color Space Normalization**: Convert to RGB for consistent processing
2. **Adaptive Resizing**: Lanczos interpolation preserves image quality
3. **Compression Optimization**: JPEG quality=85 balances size vs fidelity
4. **Base64 Encoding**: Efficient API transport format

Zero-Shot Classification Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our approach uses carefully designed candidate labels to capture different types of image content:

.. list-table:: Candidate Label Strategy
   :header-rows: 1
   :widths: 30 70

   * - Label
     - Purpose
   * - ``"AI-generated image"``
     - Direct detection of AI-generated content
   * - ``"photograph"``
     - Real photo classification baseline
   * - ``"digital art"``
     - Artistic AI content (DALL-E, Midjourney style)
   * - ``"3D render"``
     - Computer graphics and 3D generated content
   * - ``"illustration"``
     - Hand-drawn or digital artwork

Classification Logic with Confidence Calibration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def classify_with_calibration(clip_scores):
       """
       Intelligent aggregation and confidence calibration
       """
       # Aggregate AI-related scores
       ai_score = max(
           clip_scores["AI-generated image"],
           clip_scores["digital art"], 
           clip_scores["3D render"],
           clip_scores["illustration"]
       )
       
       photo_score = clip_scores["photograph"]
       
       # Decision boundary with confidence calibration
       if ai_score >= max(0.55, photo_score + 0.1):
           label = "ai"
           # Conservative confidence to avoid false accusations
           confidence = min(0.95, max(0.6, ai_score))
       else:
           label = "real"
           confidence = min(0.95, max(0.55, photo_score))
       
       return {
           "label": label,
           "confidence": confidence,
           "raw_scores": clip_scores
       }

Advanced Computer Vision Concepts
---------------------------------

Vision Transformer (ViT) Advantages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Global Receptive Field**
   Unlike CNNs with local receptive fields, ViTs process all image patches simultaneously through self-attention, capturing long-range dependencies crucial for detecting subtle AI artifacts.

**Attention Mechanisms**
   Multi-head self-attention allows the model to focus on relevant image regions and understand spatial relationships across the entire image.

.. code-block:: python

   def multi_head_attention(query, key, value, num_heads=12):
       """
       Simplified multi-head attention mechanism
       """
       batch_size, seq_len, embed_dim = query.shape
       head_dim = embed_dim // num_heads
       
       # Split into multiple heads
       q = query.view(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)
       k = key.view(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)
       v = value.view(batch_size, seq_len, num_heads, head_dim).transpose(1, 2)
       
       # Scaled dot-product attention
       scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(head_dim)
       attention_weights = F.softmax(scores, dim=-1)
       attended_values = torch.matmul(attention_weights, v)
       
       # Concatenate heads
       output = attended_values.transpose(1, 2).contiguous().view(
           batch_size, seq_len, embed_dim
       )
       
       return output, attention_weights

**Robustness to Adversarial Attacks**
   Vision Transformers are generally more robust to adversarial perturbations compared to CNNs, making them suitable for adversarial-aware applications.

Multimodal Embedding Space
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Contrastive Learning (InfoNCE Loss)**

.. math::

   \mathcal{L} = -\log \frac{\exp(\text{sim}(z_i, z_j) / \tau)}{\sum_{k=1}^{N} \exp(\text{sim}(z_i, z_k) / \tau)}

Where:
- :math:`z_i` is the image embedding
- :math:`z_j` is the corresponding text embedding  
- :math:`\tau` is the temperature parameter
- :math:`\text{sim}(·,·)` is cosine similarity

**Semantic Understanding**
   CLIP learns to map visual concepts to natural language, enabling semantic reasoning about image content rather than just visual pattern matching.

Performance Optimizations
--------------------------

Caching Strategy
~~~~~~~~~~~~~~~~

.. code-block:: python

   from collections import OrderedDict
   
   class LRUCache:
       def __init__(self, max_size=500):
           self.cache = OrderedDict()
           self.max_size = max_size
       
       def get(self, key):
           if key in self.cache:
               # Move to end (most recently used)
               self.cache.move_to_end(key)
               return self.cache[key]
           return None
       
       def set(self, key, value):
           self.cache[key] = value
           self.cache.move_to_end(key)
           
           # Remove oldest items if over capacity
           while len(self.cache) > self.max_size:
               self.cache.popitem(last=False)

API Resilience
~~~~~~~~~~~~~~

.. code-block:: python

   async def resilient_api_call(url, payload, max_retries=3):
       """
       Robust API calling with exponential backoff
       """
       for attempt in range(max_retries):
           try:
               response = await asyncio.wait_for(
                   aiohttp.post(url, json=payload), 
                   timeout=18.0
               )
               
               if response.status == 200:
                   return await response.json()
               elif response.status in [502, 503, 504]:
                   # Transient server errors - retry with backoff
                   await asyncio.sleep(0.5 * (2 ** attempt))
                   continue
               else:
                   # Permanent error - don't retry
                   break
                   
           except asyncio.TimeoutError:
               if attempt < max_retries - 1:
                   await asyncio.sleep(0.5 * (2 ** attempt))
                   continue
               raise
       
       raise APIError(f"Failed after {max_retries} attempts")

Model Warmup
~~~~~~~~~~~~

.. code-block:: python

   def warmup_model(api_key):
       """
       Reduce cold-start latency with dummy request
       """
       try:
           dummy_payload = {
               "inputs": "data:image/jpeg;base64,warmup_token",
               "parameters": {"candidate_labels": ["test"]}
           }
           
           # Fire-and-forget warmup request
           requests.post(
               "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32",
               json=dummy_payload,
               headers={"Authorization": f"Bearer {api_key}"},
               timeout=3
           )
       except:
           pass  # Warmup failure is non-critical

Evaluation and Validation
--------------------------

Performance Metrics
~~~~~~~~~~~~~~~~~~~

**Classification Metrics:**

.. code-block:: python

   def evaluate_model(predictions, ground_truth):
       """
       Comprehensive evaluation metrics
       """
       from sklearn.metrics import (
           accuracy_score, precision_recall_fscore_support,
           roc_auc_score, classification_report
       )
       
       # Basic metrics
       accuracy = accuracy_score(ground_truth, predictions)
       precision, recall, f1, _ = precision_recall_fscore_support(
           ground_truth, predictions, average='weighted'
       )
       
       # ROC-AUC for probability calibration
       auc = roc_auc_score(ground_truth, prediction_probabilities)
       
       return {
           'accuracy': accuracy,
           'precision': precision,
           'recall': recall,
           'f1_score': f1,
           'auc': auc
       }

**Calibration Analysis:**

.. code-block:: python

   def calibration_curve(y_true, y_prob, n_bins=10):
       """
       Reliability diagram for confidence calibration
       """
       bin_boundaries = np.linspace(0, 1, n_bins + 1)
       bin_lowers = bin_boundaries[:-1]
       bin_uppers = bin_boundaries[1:]
       
       accuracies = []
       confidences = []
       
       for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
           in_bin = (y_prob > bin_lower) & (y_prob <= bin_upper)
           prop_in_bin = in_bin.mean()
           
           if prop_in_bin > 0:
               accuracy_in_bin = y_true[in_bin].mean()
               avg_confidence_in_bin = y_prob[in_bin].mean()
               accuracies.append(accuracy_in_bin)
               confidences.append(avg_confidence_in_bin)
       
       return np.array(accuracies), np.array(confidences)

Ethical Considerations
----------------------

Bias Mitigation
~~~~~~~~~~~~~~~

**Dataset Diversity**
   CLIP was trained on diverse internet images, but we monitor for potential biases in specific domains or demographics.

**Fairness Metrics**
   Evaluate performance across different image types, styles, and cultural contexts to ensure equitable classification.

**Transparency**
   Clearly communicate model limitations and confidence scores to users.

Privacy Protection
~~~~~~~~~~~~~~~~~~

**Data Minimization**
   - Images processed temporarily server-side
   - No persistent storage of image content
   - Only image URLs transmitted, not pixel data

**User Consent**
   - Clear disclosure of analysis functionality
   - Opt-in extension installation
   - Configurable API endpoints for user control

Responsible AI Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~

**Conservative Thresholds**
   - High bar for AI classification (0.55+ threshold)
   - Maximum confidence capped at 95%
   - Clear uncertainty communication

**Human Oversight**
   - Enable manual review for disputed cases
   - Provide reasoning through confidence scores
   - Support appeals process for content creators

Future Enhancements
-------------------

Model Improvements
~~~~~~~~~~~~~~~~~~

**Ensemble Methods**
   Combine CLIP with specialized AI detection models for improved accuracy.

**Fine-tuning**
   Domain adaptation on curated AI detection datasets while preserving generalization.

**Larger Models**
   Upgrade to CLIP-ViT-Large-Patch14 for improved accuracy with acceptable latency trade-offs.

Advanced Techniques
~~~~~~~~~~~~~~~~~~~

**Attention Visualization**
   Show which image regions drive classification decisions for interpretability.

**Uncertainty Quantification**
   Bayesian approaches for better confidence estimation and out-of-distribution detection.

**Adversarial Training**
   Robustness improvements against evasion attacks and adversarial examples.
