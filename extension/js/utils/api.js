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

    async getSessionInfo(accountId) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/accounts/${accountId}/session`, {
            headers: {
                'Authorization': `Bearer ${token.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch session info');
        }

        return response.json();
    }

    async createSession(accountId, domain) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/sessions`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                account_id: accountId,
                domain: domain
            })
        });

        if (!response.ok) {
            throw new Error('Failed to create session');
        }

        return response.json();
    }

    async updateSession(accountId, domain) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/sessions/${accountId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                domain: domain
            })
        });

        if (!response.ok) {
            throw new Error('Failed to update session');
        }

        return response.json();
    }

    async removeSession(accountId, domain) {
        const token = await chrome.storage.local.get('token');
        if (!token.token) {
            throw new Error('No authentication token');
        }

        const response = await fetch(`${API_URL}/api/sessions/${accountId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to remove session');
        }

        return response.json();
    }
}

export const api = new Api();