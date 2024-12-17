export const API_URL = 'https://api.artutos.us.kg';

export const SESSION_CONFIG = {
    INACTIVITY_TIMEOUT: 60000, // 1 minute
    MAX_CONCURRENT_SESSIONS: 3,
    REFRESH_INTERVAL: 30000 // 30 seconds
};

export const UI_CONFIG = {
    ERROR_TIMEOUT: 5000,
    SUCCESS_TIMEOUT: 3000
};

export const STORAGE_KEYS = {
    TOKEN: 'token',
    CURRENT_ACCOUNT: 'currentAccount',
    USER_DATA: 'userData'
};

export const ANALYTICS_CONFIG = {
    TRACKING_INTERVAL: 60000, // 1 minute
    BATCH_SIZE: 10,
    INACTIVITY_TIMEOUT: 300000 // 5 minutes
};