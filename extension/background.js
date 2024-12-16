chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'GET_CURRENT_ACCOUNT') {
    chrome.storage.local.get(['currentAccount'], result => {
      sendResponse(result.currentAccount);
    });
    return true;
  }
});

// Manejar cambios en la configuración del proxy
chrome.proxy.settings.onChange.addListener((details) => {
  console.log('Proxy settings changed:', details);
});

// Manejar errores de proxy
chrome.proxy.onProxyError.addListener((details) => {
  console.error('Proxy error:', details);
});