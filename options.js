document.addEventListener('DOMContentLoaded', async () => {
  const apiUrlInput = document.getElementById('apiUrl');
  const apiKeyInput = document.getElementById('apiKey');
  const statusEl = document.getElementById('status');

  const saved = await chrome.storage.sync.get({ apiUrl: '', apiKey: '' });
  apiUrlInput.value = saved.apiUrl || '';
  apiKeyInput.value = saved.apiKey || '';

  document.getElementById('save').addEventListener('click', async () => {
    const apiUrl = apiUrlInput.value.trim();
    const apiKey = apiKeyInput.value.trim();
    await chrome.storage.sync.set({ apiUrl, apiKey });
    statusEl.textContent = 'Saved settings.';
    statusEl.style.color = '#059669';
  });

  // Quick POST test to verify your endpoint accepts our schema
  document.getElementById('test').addEventListener('click', async () => {
    const apiUrl = apiUrlInput.value.trim();
    const apiKey = apiKeyInput.value.trim();
    if (!apiUrl) {
      statusEl.textContent = 'Enter an API URL first.';
      statusEl.style.color = '#b91c1c';
      return;
    }
    try {
      const resp = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {})
        },
        body: JSON.stringify({ imageUrl: 'https://example.com/example.jpg' })
      });
      const text = await resp.text();
      statusEl.textContent = `Response (${resp.status}): ${text.slice(0, 200)}...`;
      statusEl.style.color = resp.ok ? '#059669' : '#b45309';
    } catch (e) {
      statusEl.textContent = `Error: ${String(e)}`;
      statusEl.style.color = '#b91c1c';
    }
  });
});
