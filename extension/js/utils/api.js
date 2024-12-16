import { API_URL } from '../config.js';

class Api {
    async login(email, password) {
        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
        });
        
        if (!response.ok) {
            throw new Error('Invalid credentials');
        }
        
        return response.json();
    }

    async getAccounts(token) {
        const response = await fetch(`${API_URL}/api/accounts`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch accounts');
        }
        
        return response.json();
    }

    async getAccountStatus(accountId) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/accounts/${accountId}/status`, {
            headers: {
                'Authorization': `Bearer ${token.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch account status');
        }

        return response.json();
    }

    async startSession(accountId) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/accounts/session/${accountId}/start`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to start session');
        }

        return response.json();
    }

    async endSession(accountId) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/accounts/session/${accountId}/end`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to end session');
        }

        return response.json();
    }

    async updateActivity(accountId, domain) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/accounts/activity/${accountId}?domain=${encodeURIComponent(domain)}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to update activity');
        }

        return response.json();
    }
}

export const api = new Api();