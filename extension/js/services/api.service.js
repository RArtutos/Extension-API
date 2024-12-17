import { API_URL } from '../config.js';
import { storage } from '../utils/storage.js';

class ApiService {
    constructor() {
        this.baseUrl = API_URL;
    }

    async getHeaders() {
        const token = await storage.get('token');
        return {
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
        };
    }

    async handleResponse(response) {
        if (!response.ok) {
            if (response.status === 401) {
                await storage.remove(['token', 'currentAccount']);
                throw new Error('unauthorized');
            }
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Request failed');
        }
        return response.json();
    }

    async login(email, password) {
        const response = await fetch(`${this.baseUrl}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
        });
        
        return this.handleResponse(response);
    }

    async getAccounts() {
        const response = await fetch(`${this.baseUrl}/api/accounts`, {
            headers: await this.getHeaders()
        });
        
        return this.handleResponse(response);
    }

    async getSessionInfo(accountId) {
        const response = await fetch(`${this.baseUrl}/api/accounts/${accountId}/session`, {
            headers: await this.getHeaders()
        });

        return this.handleResponse(response);
    }

    async createSession(accountId, domain) {
        const response = await fetch(`${this.baseUrl}/api/sessions`, {
            method: 'POST',
            headers: await this.getHeaders(),
            body: JSON.stringify({ account_id: accountId, domain })
        });

        return this.handleResponse(response);
    }

    async updateSession(accountId, domain) {
        const response = await fetch(`${this.baseUrl}/api/sessions/${accountId}`, {
            method: 'PUT',
            headers: await this.getHeaders(),
            body: JSON.stringify({ domain })
        });

        return this.handleResponse(response);
    }

    async endSession(accountId) {
        const response = await fetch(`${this.baseUrl}/api/sessions/${accountId}`, {
            method: 'DELETE',
            headers: await this.getHeaders()
        });

        return this.handleResponse(response);
    }
}

export const apiService = new ApiService();