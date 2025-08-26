(function() {
  const OVERLAY_CLASS = 'image-ai-detector-overlay';
  const BADGE_CLASS = 'image-ai-detector-badge';

  const pendingRequests = new Map();
  const REQUEST_TIMEOUT_MS = 15000; // Per-image timeout to avoid hanging badges

  function isVisibleInViewport(element) {
    const rect = element.getBoundingClientRect();
    const inViewport = (
      rect.bottom > 0 &&
      rect.right > 0 &&
      rect.left < (window.innerWidth || document.documentElement.clientWidth) &&
      rect.top < (window.innerHeight || document.documentElement.clientHeight)
    );
    const hasSize = rect.width >= 32 && rect.height >= 32;
    const style = window.getComputedStyle(element);
    const visibleStyle = style.visibility !== 'hidden' && style.display !== 'none' && Number(style.opacity) > 0.01;
    return inViewport && hasSize && visibleStyle;
  }

  // Create the on-image overlay and initial badge
  function createOverlayForImage(img) {
    const rect = img.getBoundingClientRect();
    const overlay = document.createElement('div');
    overlay.className = OVERLAY_CLASS;
    overlay.style.position = 'absolute';
    overlay.style.left = `${window.scrollX + rect.left}px`;
    overlay.style.top = `${window.scrollY + rect.top}px`;
    overlay.style.width = `${rect.width}px`;
    overlay.style.height = `${rect.height}px`;
    overlay.style.pointerEvents = 'none';
    overlay.style.zIndex = '2147483646';

    const badge = document.createElement('div');
    badge.className = BADGE_CLASS;
    badge.style.position = 'absolute';
    badge.style.left = '8px';
    badge.style.top = '8px';
    badge.style.padding = '4px 8px';
    badge.style.borderRadius = '999px';
    badge.style.fontSize = '12px';
    badge.style.fontFamily = 'ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial';
    badge.style.fontWeight = '600';
    badge.style.color = '#fff';
    badge.style.background = 'rgba(0,0,0,0.6)';
    badge.style.backdropFilter = 'blur(4px)';
    badge.style.pointerEvents = 'auto';
    badge.style.cursor = 'default';
    badge.textContent = 'Analyzing…';

    overlay.appendChild(badge);
    document.body.appendChild(overlay);

    return { overlay, badge };
  }

  function updateOverlayPosition(img, overlay) {
    const rect = img.getBoundingClientRect();
    overlay.style.left = `${window.scrollX + rect.left}px`;
    overlay.style.top = `${window.scrollY + rect.top}px`;
    overlay.style.width = `${rect.width}px`;
    overlay.style.height = `${rect.height}px`;
  }

  // Update the badge UI based on the classification result
  function setBadgeResult(badge, result) {
    const { label, confidence } = result;
    const pct = Math.round(confidence * 100);
    if (label === 'ai') {
      badge.style.background = 'linear-gradient(135deg, #a21caf, #7c3aed)';
      badge.textContent = `AI-generated • ${pct}%`;
    } else {
      badge.style.background = 'linear-gradient(135deg, #059669, #10b981)';
      badge.textContent = `Real • ${pct}%`;
    }
  }

  function analyzeVisibleImages() {
    const images = Array.from(document.images).filter(isVisibleInViewport);

    images.forEach((img, index) => {
      const src = img.currentSrc || img.src;
      if (!src) return;

      const { overlay, badge } = createOverlayForImage(img);

      const requestId = `${Date.now()}-${index}-${Math.random().toString(36).slice(2,8)}`;
      pendingRequests.set(requestId, { img, overlay, badge });

      chrome.runtime.sendMessage({
        type: 'DETECT_IMAGE_URL',
        payload: { imageUrl: src, requestId }
      });

      // Set a timeout fail-safe so badge won't hang forever
      const timeoutId = setTimeout(() => {
        const entry = pendingRequests.get(requestId);
        if (!entry) return;
        entry.badge.style.background = 'linear-gradient(135deg, #b91c1c, #ef4444)';
        entry.badge.textContent = 'Timed out';
        entry.overlay.style.boxShadow = 'inset 0 0 0 2px rgba(255,255,255,0.6)';
        pendingRequests.delete(requestId);
      }, REQUEST_TIMEOUT_MS);

      const onScrollOrResize = () => updateOverlayPosition(img, overlay);
      window.addEventListener('scroll', onScrollOrResize, { passive: true });
      window.addEventListener('resize', onScrollOrResize);

      const observer = new ResizeObserver(() => updateOverlayPosition(img, overlay));
      observer.observe(img);

      // Cleanup when image is removed from DOM
      const mutationObserver = new MutationObserver(() => {
        if (!document.body.contains(img)) {
          overlay.remove();
          observer.disconnect();
          mutationObserver.disconnect();
          window.removeEventListener('scroll', onScrollOrResize);
          window.removeEventListener('resize', onScrollOrResize);
        }
      });
      mutationObserver.observe(document.body, { childList: true, subtree: true });

      // Store timeout id for clearing on success
      pendingRequests.get(requestId).timeoutId = timeoutId;
    });
  }

  chrome.runtime.onMessage.addListener((message) => {
    if (message?.type === 'ANALYZE_IMAGES') {
      analyzeVisibleImages();
    } else if (message?.type === 'DETECTION_RESULT') {
      const { requestId, result } = message.payload || {};
      const entry = pendingRequests.get(requestId);
      if (entry) {
        // Clear timeout if set
        if (entry.timeoutId) clearTimeout(entry.timeoutId);
        setBadgeResult(entry.badge, result);
        // Fade in outline for clarity
        entry.overlay.style.boxShadow = 'inset 0 0 0 2px rgba(255,255,255,0.8)';
        pendingRequests.delete(requestId);
      }
    }
  });
})();
