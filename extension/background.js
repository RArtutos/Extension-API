// Background Script
let currentProfile = null;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'SWITCH_PROFILE') {
    switchProfile(request.profileId);
  }
});

async function switchProfile(profileId) {
  try {
    const token = await new Promise(resolve => {
      chrome.storage.local.get(['token'], result => resolve(result.token));
    });

    const response = await fetch(`http://localhost:3000/api/profiles/${profileId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const profile = await response.json();
    currentProfile = profile;

    // Apply cookies
    for (const cookie of profile.cookies) {
      await chrome.cookies.set({
        url: `https://${cookie.domain}`,
        name: cookie.name,
        value: cookie.value,
        path: cookie.path,
        domain: cookie.domain,
      });
    }

    // Apply proxy settings if available
    if (profile.proxy) {
      const config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            host: profile.proxy.host,
            port: profile.proxy.port,
          },
        },
      };

      await chrome.proxy.settings.set({
        value: config,
        scope: 'regular',
      });
    }
  } catch (error) {
    console.error('Failed to switch profile:', error);
  }
}