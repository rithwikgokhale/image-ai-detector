document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyze');
  const openOptions = document.getElementById('openOptions');

  analyzeBtn?.addEventListener('click', () => {
    chrome.runtime.sendMessage({ type: 'ANALYZE_ACTIVE_TAB' }, (resp) => {
      // Optional: Could show a toast in the popup, but popup will close soon after
    });
    window.close();
  });

  openOptions?.addEventListener('click', (e) => {
    e.preventDefault();
    if (chrome.runtime.openOptionsPage) {
      chrome.runtime.openOptionsPage();
    } else {
      window.open('options.html');
    }
  });
});
