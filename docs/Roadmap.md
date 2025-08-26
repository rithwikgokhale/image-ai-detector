### Roadmap

#### Short Term
- Add batch requests: `POST /classify-batch` for multiple URLs
- Client-side caching keyed by image URL or perceptual hash
- Optional auto-analyze on page load, with rate limits
- Try stronger detectors (e.g., specialized AI/real classifiers) and prompt/label tuning for CLIP

#### Medium Term
- Switch to EfficientNet or ConvNeXt backbones
- Hard-negative mining; adversarial training loops
- Model versioning and A/B experiments
- Ensemble CLIP with a second classifier; confidence calibration

#### Long Term
- In-browser inference (WebGPU/WASM, ONNX Runtime Web)
- Vision-language cross-checks (CLIP, Q-Former variants)
- Multi-signal authenticity (EXIF, watermark detection, provenance)

#### Developer Experience
- CLI for packaging and test-driving the extension
- GitHub Actions for lint/test/build on PRs
- Telemetry hooks (opt-in, anonymized) for error/latency
