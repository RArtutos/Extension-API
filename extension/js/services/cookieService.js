import { parseHeaderString } from '../utils/cookieParser.js';
import { COOKIE_DEFAULTS } from '../config.js';

class CookieService {
  async setCookie(domain, name, value, options = {}) {
    const cleanDomain = domain.startsWith('.') ? domain.substring(1) : domain;
    const url = `https://${cleanDomain}`;
    
    const cookieData = {
      url,
      name,
      value,
      domain,
      ...COOKIE_DEFAULTS,
      ...options
    };

    try {
      await chrome.cookies.set(cookieData);
    } catch (error) {
      console.warn(`Error setting cookie ${name}, retrying with alternative settings:`, error);
      try {
        await chrome.cookies.set({
          ...cookieData,
          domain: cleanDomain,
          secure: false,
          sameSite: 'no_restriction'
        });
      } catch (retryError) {
        console.error(`Failed to set cookie ${name} after retry:`, retryError);
        throw retryError;
      }
    }
  }

  async removeAllCookies(domain) {
    if (!domain) return;
    
    const cleanDomain = domain.startsWith('.') ? domain.substring(1) : domain;
    const cookies = await chrome.cookies.getAll({ domain: cleanDomain });
    
    for (const cookie of cookies) {
      try {
        await chrome.cookies.remove({
          url: `https://${cleanDomain}${cookie.path || '/'}`,
          name: cookie.name,
          storeId: cookie.storeId
        });
      } catch (error) {
        console.warn(`Error removing cookie ${cookie.name}:`, error);
      }
    }
  }

  async processHeaderString(domain, cookieString) {
    if (!cookieString) return;
    
    const cookies = parseHeaderString(cookieString);
    for (const cookie of cookies) {
      await this.setCookie(domain, cookie.name, cookie.value);
    }
  }
}

export const cookieService = new CookieService();