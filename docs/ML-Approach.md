### ML Approach

#### Problem Definition
- Task: Binary classification → AI-generated vs Real
- Input: Image URL (downloaded server-side for inference)
- Output: `{ label: 'ai'|'real', confidence: 0..1 }`

#### Baseline Model
- CNN backbone (TensorFlow/Keras), softmax over 2 classes
- Lightweight for low-latency API inference

#### Feature Engineering (Optional Ensemble)
- Edge density, color channel moments, LBP variance
- Combine with CNN logits via averaging or a small fusion layer

#### Training Pipeline
- `train_model.py`: Example dataset builder, generators, callbacks
- Early stopping, LR schedule, model checkpointing
- Data augmentation recommended (not fully shown)

#### Evaluation
- Metrics: Accuracy, Precision/Recall, ROC-AUC
- Calibration: Confidence reflects probability (reliability curves)
- Bias checks: Ensure no spurious correlations (e.g., watermarking, compression level)

#### Deployment
- `simple_ai_detector.py`: Flask API exposing `/classify` (default)
- Request: `{ imageUrl }`; Response: `{ label, confidence }`
- Current default server uses zero‑shot CLIP (labels like "AI‑generated image" vs "photograph"), with image downscaling and retry for reliability
- Optimizations: TFLite quantization, batching

#### Limitations & Risks
- Generalization to novel generators (diffusion model versions)
- Adversarial adaptations to evade detectors
- Dataset curation: coverage, balance, and labeling noise

#### Roadmap for Accuracy
- Transfer learning from strong backbones (e.g., EfficientNet)
- Hard-negative mining; adversarial training
- Periodic re-training with freshly generated data
- Ensemble across multiple detectors

#### Ethical Considerations
- False positives have reputational impact (be conservative)
- Explain limitations; expose confidence and thresholds
- Respect privacy and terms when fetching images server-side
