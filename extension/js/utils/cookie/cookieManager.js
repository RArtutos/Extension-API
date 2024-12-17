import { CookiePermissions } from './cookiePermissions.js';
import { CookieParser } from './cookieParser.js';
import { CookieSetter } from './cookieSetter.js';

class CookieManager {
  constructor() {
    this.permissions = new CookiePermissions();
    this.parser = new CookieParser();
    this.setter = new CookieSetter();
  }

  async setAccountCookies(account) {
    if (!account?.cookies?.length) {
      console.warn('No cookies found for account');
      return;
    }

    try {
      // No need to request permissions as they are now in manifest
      for (const cookie of account.cookies) {
        const domain = cookie.domain;
        await this.removeAllCookiesForDomain(domain);

        if (cookie.name === 'header_cookies') {
          await this.setHeaderCookies(domain, cookie.value);
        } else {
          await this.setter.setCookie(domain, cookie.name, cookie.value);
        }
      }
    } catch (error) {
      console.error('Error setting account cookies:', error);
      throw new Error('Failed to set account cookies');
    }
  }

  async setHeaderCookies(domain, cookieString) {
    const cookies = this.parser.parseHeaderString(cookieString);
    for (const cookie of cookies) {
      await this.setter.setCookie(domain, cookie.name, cookie.value);
    }
  }

  async removeAccountCookies(account) {
    if (!account?.cookies?.length) return;
    
    for (const cookie of account.cookies) {
      await this.removeAllCookiesForDomain(cookie.domain);
    }
  }

  async removeAllCookiesForDomain(domain) {
    const cleanDomain = domain.startsWith('.') ? domain.substring(1) : domain;
    const cookies = await chrome.cookies.getAll({ domain: cleanDomain });
    
    for (const cookie of cookies) {
      try {
        await chrome.cookies.remove({
          url: `https://${cleanDomain}`,
          name: cookie.name
        });
      } catch (error) {
        console.warn(`Error removing cookie ${cookie.name}:`, error);
      }
    }
  }
}

export const cookieManager = new CookieManager();