import { API_URL } from '../config.js';
import { storage } from '../utils/storage.js';
import { STORAGE_KEYS } from '../config.js';

class ApiService {
    constructor() {
        this.baseUrl = API_URL;
    }

    async getHeaders() {
        const token = await storage.get(STORAGE_KEYS.TOKEN);
        return {
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
        };
    }

    async validateToken(token) {
        try {
            const response = await fetch(`${this.baseUrl}/api/auth/validate`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Invalid token');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Token validation failed:', error);
            return null;
        }
    }

    async login(email, password) {
        try {
            const response = await fetch(`${this.baseUrl}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            if (!data.access_token) {
                throw new Error('Invalid response from server');
            }

            // Store the token
            await storage.set(STORAGE_KEYS.TOKEN, data.access_token);
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async getAccounts() {
        try {
            const headers = await this.getHeaders();
            const response = await fetch(`${this.baseUrl}/api/accounts`, {
                headers
            });

            if (!response.ok) {
                if (response.status === 401) {
                    // Clear invalid token
                    await storage.remove(STORAGE_KEYS.TOKEN);
                }
                throw new Error('Failed to fetch accounts');
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching accounts:', error);
            throw error;
        }
    }
}

export const apiService = new ApiService();