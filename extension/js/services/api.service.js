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

        return data;
    }

    // ... resto del código ...
}

export const apiService = new ApiService();