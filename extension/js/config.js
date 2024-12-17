// API configuration
export const API_URL = 'https://api.artutos.us.kg';

// Cookie configuration
export const COOKIE_DEFAULTS = {
  path: '/',
  secure: true,
  sameSite: 'lax',
  maxAge: 3600 * 24 // 24 hours
};

// Storage keys
export const STORAGE_KEYS = {
  TOKEN: 'token',
  CURRENT_ACCOUNT: 'currentAccount',
  PROXY_ENABLED: 'proxyEnabled',
  USER_SETTINGS: 'userSettings'
};

// Session configuration
export const SESSION_CONFIG = {
  INACTIVITY_TIMEOUT: 60000, // 1 minute in milliseconds
  MAX_CONCURRENT_SESSIONS: 3
};

// UI configuration
export const UI_CONFIG = {
  ERROR_TIMEOUT: 5000,    // How long error messages show
  SUCCESS_TIMEOUT: 3000,  // How long success messages show
  REFRESH_INTERVAL: 30000 // How often to refresh account status
};

// Feature flags
export const FEATURES = {
  PROXY_ENABLED: true,
  ANALYTICS_ENABLED: true,
  AUTO_REFRESH: true
};