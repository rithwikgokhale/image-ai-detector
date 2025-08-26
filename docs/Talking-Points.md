### Interview Talking Points

#### Product Value
- One-click visibility into potential AI-generated content on any page
- Developer-friendly: pluggable backend, robust fallback, clear API

#### Architecture Strengths
- Clean MV3 separation: popup, background, content script
- Resilient message-passing; no tab/thread coupling
- Inline overlay rendering that survives layout changes

#### ML Positioning
- Start simple (CNN baseline + stats) → iterate to ensembles
- Measurable metrics (precision/recall) and calibration focus
- Explicit limitations; confidence shown to the user

#### Trade-offs & Decisions
- Server-side inference vs on-device: latency vs capability
  - Current server: `simple_ai_detector.py` (HTTP on :5001)
- Deterministic mock: instant demo, reliable DX
- Inline styles for overlays: maximal cross-site compatibility

#### Scaling Plan
- Batch inference; CDN caching by image hash
  - Add `/classify-batch` endpoint and client aggregation
- Dedicated inference workers and autoscaling
- Model retraining cadence with drift monitoring

#### Ethics & UX
- Avoid definitive claims; expose confidence and thresholds
- Clear language—"Likely AI-generated" vs "AI"
- Respect privacy; don’t transmit images themselves unless necessary
