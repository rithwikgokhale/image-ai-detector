### Architecture

#### Components
- **Popup (`popup.html`/`popup.js`)**: Minimal UI for triggering analysis and opening settings.
- **Background Service Worker (`background.js`)**: Central orchestrator. Receives analysis requests, calls the ML API or mock, sends results to the active tab.
- **Content Script (`content-script.js`)**: Discovers visible images, creates/positions overlays, updates badges on results.
- **Options Page (`options.html`/`options.js`)**: Persists `apiUrl` and optional `apiKey` to `chrome.storage.sync`. Default API URL now points to `http://localhost:5001/classify`.

#### Data Flow
1. User clicks the extension → Popup opens
2. User clicks "Analyze" → Popup sends `{ type: 'ANALYZE_ACTIVE_TAB' }` to background
3. Background sends `{ type: 'ANALYZE_IMAGES' }` to the content script in the active tab
4. Content script finds visible images and for each image:
   - Builds overlay with "Analyzing…" badge
   - Sends `{ type: 'DETECT_IMAGE_URL', imageUrl, requestId }` to background
5. Background calls ML API (or mock) → receives `{ label, confidence }`
6. Background sends `{ type: 'DETECTION_RESULT', requestId, result }` to content script
7. Content script updates the corresponding badge and overlay

#### Sequence (text)
- Popup → Background: Analyze Active Tab
- Background → Content Script: Analyze Images
- Content Script → Background: Detect Image URL x N
- Background → Local Server: POST /classify x N (defaults to http://localhost:5001)
- Local Server → Hugging Face: Inference API request
- Local Server → Background: JSON result x N
- Background → Content Script: Detection Result x N

#### Permissions & Security
- `activeTab`, `scripting`, `tabs`, `storage` for MV3
- Host permissions: `<all_urls>` to support most sites
- API key stored via `chrome.storage.sync` (not perfect security; server must enforce proper auth/rate limits)

#### Reliability & UX Considerations
- Mock classifier fallback if API fails or is unset
- Background fetches include explicit timeouts to avoid hanging UI
- Content script shows "Timed out" if no result arrives within 15s
- Inline styles ensure overlays render predictably across sites
- Observers keep badges positioned on scroll/resize/layout changes

#### Extensibility
- Swap ML backend by changing `apiUrl`
- Add batching or debounce in background SW
- Add context menus or auto-analyze on page load
