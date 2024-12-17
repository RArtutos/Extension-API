import { analyticsService } from './js/services/analyticsService.js';
import { storage } from './js/utils/storage.js';

// Track tab activity
chrome.tabs.onActivated.addListener(async (activeInfo) => {
    try {
        const tab = await chrome.tabs.get(activeInfo.tabId);
        if (tab.url) {
            const domain = new URL(tab.url).hostname;
            analyticsService.resetTimer(domain);
        }
    } catch (error) {
        console.error('Error handling tab activation:', error);
    }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    try {
        if (changeInfo.url) {
            const domain = new URL(changeInfo.url).hostname;
            analyticsService.resetTimer(domain);
        }
    } catch (error) {
        console.error('Error handling tab update:', error);
    }
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'GET_CURRENT_ACCOUNT') {
        storage.get('currentAccount').then(account => {
            sendResponse(account);
        });
        return true;
    }
});

// Handle proxy settings
chrome.proxy.settings.onChange.addListener((details) => {
    console.log('Proxy settings changed:', details);
});

chrome.proxy.onProxyError.addListener((details) => {
    console.error('Proxy error:', details);
});