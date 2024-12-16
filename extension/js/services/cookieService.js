class CookieService {
  async setAccountCookies(account) {
    for (const cookie of account.cookies) {
      const domain = cookie.domain;
      
      // Remove existing cookies first
      await this.removeAllCookiesForDomain(domain);

      // Set new cookies
      if (cookie.name === 'header_cookies') {
        await this.setHeaderCookies(domain, cookie.value);
      }
    }
  }

  async setHeaderCookies(domain, cookieString) {
    const cookies = this.parseHeaderString(cookieString);
    for (const cookie of cookies) {
      await this.setCookie(domain, cookie.name, cookie.value);
    }
  }

  async setCookie(domain, name, value) {
    const cleanDomain = domain.startsWith('.') ? domain.substring(1) : domain;
    const url = `https://${cleanDomain}`;
    
    try {
      await chrome.cookies.set({
        url,
        name,
        value,
        domain,
        path: '/',
        secure: true,
        sameSite: 'lax'
      });
    } catch (error) {
      console.warn(`Error setting cookie ${name}:`, error);
    }
  }

  async removeAllCookiesForDomain(domain) {
    const cookies = await chrome.cookies.getAll({ domain });
    for (const cookie of cookies) {
      try {
        const cleanDomain = domain.startsWith('.') ? domain.substring(1) : domain;
        await chrome.cookies.remove({
          url: `https://${cleanDomain}`,
          name: cookie.name
        });
      } catch (error) {
        console.warn(`Error removing cookie ${cookie.name}:`, error);
      }
    }
  }

  parseHeaderString(cookieString) {
    if (!cookieString) return [];
    
    const cookies = [];
    const pairs = cookieString.split(';');
    
    for (const pair of pairs) {
      const [name, value] = pair.trim().split('=');
      if (name && value) {
        cookies.push({ name: name.trim(), value: value.trim() });
      }
    }
    
    return cookies;
  }
}

export const cookieService = new CookieService();