// Background service worker (MV3)

/**
 * Deterministic mock classifier based on URL hash.
 * If options.apiUrl is set, attempts to call external API instead.
 *
 * Network requests use an explicit timeout to prevent the UI from hanging.
 */
const FETCH_TIMEOUT_MS = 12000; // Abort API calls that take too long

async function fetchWithTimeout(url, options = {}, timeoutMs = FETCH_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}
async function classifyImageByUrl(imageUrl) {
  const defaultLocalApi = 'http://localhost:5001/classify';
  const options = await chrome.storage.sync.get({ apiUrl: defaultLocalApi, apiKey: '' });
  const apiUrl = (options.apiUrl?.trim() || defaultLocalApi);
  const apiKey = options.apiKey?.trim();

  if (apiUrl) {
    try {
      const response = await fetchWithTimeout(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {})
        },
        body: JSON.stringify({ imageUrl })
      });
      if (!response.ok) throw new Error(`API ${response.status}`);
      const data = await response.json();
      // Expected shape: { label: 'ai'|'real', confidence: 0-1 }
      const label = (data.label || '').toLowerCase() === 'ai' ? 'ai' : 'real';
      const confidence = Math.max(0, Math.min(1, Number(data.confidence ?? 0.5)));
      return { label, confidence, source: apiUrl };
    } catch (error) {
      console.warn('Classifier API failed, falling back to mock:', error);
      // Fall through to mock
    }
  }

  // Mock/deterministic fallback using URL hash
  let hash = 0;
  for (let i = 0; i < imageUrl.length; i++) {
    hash = ((hash << 5) - hash) + imageUrl.charCodeAt(i);
    hash |= 0;
  }
  const isAi = (Math.abs(hash) % 2) === 0;
  const confidence = ((Math.abs(hash) % 51) + 50) / 100; // 0.5 - 1.0
  return { label: isAi ? 'ai' : 'real', confidence, source: 'mock' };
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === 'DETECT_IMAGE_URL') {
    const { imageUrl, requestId } = message.payload || {};
    (async () => {
      const result = await classifyImageByUrl(imageUrl);
      if (sender?.tab?.id != null) {
        chrome.tabs.sendMessage(sender.tab.id, {
          type: 'DETECTION_RESULT',
          payload: { requestId, imageUrl, result }
        });
      }
    })();
    sendResponse({ ok: true });
    return true;
  }

  if (message?.type === 'ANALYZE_ACTIVE_TAB') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs && tabs[0];
      if (tab && tab.id != null) {
        chrome.tabs.sendMessage(tab.id, { type: 'ANALYZE_IMAGES' });
        sendResponse({ ok: true, tabId: tab.id });
      } else {
        sendResponse({ ok: false, error: 'No active tab.' });
      }
    });
    return true; // keep message channel open for async sendResponse
  }
});
