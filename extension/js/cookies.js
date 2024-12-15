// Lista de cookies que no debemos intentar establecer
const IGNORED_COOKIES = [
  'netflix-sans-normal-3-loaded',
  'netflix-sans-bold-3-loaded'
];

export const cookieManager = {
  async requestPermissions() {
    try {
      const granted = await chrome.permissions.request({
        permissions: ['cookies'],
        origins: ['<all_urls>']
      });
      return granted;
    } catch (error) {
      console.error('Error requesting permissions:', error);
      return false;
    }
  },

  async removeCookie(url, name) {
    if (IGNORED_COOKIES.includes(name)) {
      return; // Ignorar cookies específicas
    }

    try {
      await chrome.cookies.remove({ url, name });
    } catch (error) {
      console.error(`Error removing cookie ${name}:`, error);
      // No lanzar error para cookies que no se pueden eliminar
    }
  },

  async setCookie(cookie) {
    if (IGNORED_COOKIES.includes(cookie.name)) {
      return; // Ignorar cookies específicas
    }

    try {
      const cookieParams = {
        url: `https://${cookie.domain}`,
        name: cookie.name,
        value: cookie.value,
        domain: cookie.domain,
        path: cookie.path || '/',
        secure: cookie.secure !== false, // Por defecto true si no se especifica
        httpOnly: cookie.httpOnly || false,
        sameSite: this.getSameSiteValue(cookie.sameSite),
        expirationDate: cookie.expirationDate,
        storeId: cookie.storeId || null
      };

      // Limpiar valores undefined o null
      Object.keys(cookieParams).forEach(key => 
        cookieParams[key] === undefined && delete cookieParams[key]
      );

      await chrome.cookies.set(cookieParams);
    } catch (error) {
      console.error(`Error setting cookie ${cookie.name}:`, error);
      // No lanzar error para cookies que no se pueden establecer
    }
  },

  getSameSiteValue(sameSite) {
    // Chrome espera estos valores específicos
    switch (sameSite?.toLowerCase()) {
      case 'strict': return 'strict';
      case 'lax': return 'lax';
      case 'none': return 'no_restriction';
      default: return 'no_restriction'; // valor por defecto
    }
  }
};