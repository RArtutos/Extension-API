import { parseHeaderString } from '../utils/cookieParser.js';

export class CookieService {
  async setCookie(domain, name, value, options = {}) {
    const urlDomain = `https://${domain.replace(/^\./, '')}`;
    
    const cookieData = {
      url: urlDomain,
      name,
      value,
      path: '/',
      domain: domain,
      secure: urlDomain.startsWith('https://'),
      sameSite: 'lax',
      httpOnly: false,
      ...options
    };

    try {
      await chrome.cookies.set(cookieData);
    } catch (error) {
      console.warn(`Error setting cookie ${name}:`, error);
      // Try alternative settings
      try {
        await chrome.cookies.set({
          ...cookieData,
          domain: domain.replace(/^\./, ''),
          secure: false
        });
      } catch (retryError) {
        console.error(`Failed to set cookie ${name} after retry:`, retryError);
        throw retryError;
      }
    }
  }

  async removeCookie(domain, name, storeId = null) {
    const urlDomain = `https://${domain.replace(/^\./, '')}`;
    const removeData = { url: urlDomain, name };
    if (storeId) removeData.storeId = storeId;
    
    try {
      await chrome.cookies.remove(removeData);
    } catch (error) {
      console.error(`Error removing cookie ${name}:`, error);
      throw error;
    }
  }

  async removeAllCookies(domain) {
    const existingCookies = await chrome.cookies.getAll({ domain });
    const promises = existingCookies.map(cookie => 
      this.removeCookie(domain, cookie.name, cookie.storeId)
    );
    await Promise.allSettled(promises);
  }

  async processHeaderString(domain, cookieString) {
    const cookies = parseHeaderString(cookieString);
    const promises = cookies.map(({ name, value }) => 
      this.setCookie(domain, name, value)
    );
    await Promise.allSettled(promises);
  }
}

export const cookieService = new CookieService();