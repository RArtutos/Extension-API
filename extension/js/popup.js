import { storage } from './utils/storage.js';
import { apiService } from './services/api.service.js';
import { ui } from './utils/ui.js';
import { accountManager } from './accountManager.js';

class PopupManager {
    constructor() {
        this.initialized = false;
    }

    async init() {
        if (this.initialized) return;
        
        await this.checkAuthState();
        this.attachEventListeners();
        this.initialized = true;
    }

    async checkAuthState() {
        const token = await storage.get('token');
        if (token) {
            try {
                await this.initializeAccountManager();
            } catch (error) {
                if (error.message === 'unauthorized') {
                    ui.showLoginForm();
                }
            }
        } else {
            ui.showLoginForm();
        }
    }

    attachEventListeners() {
        document.getElementById('login-btn')?.addEventListener('click', () => this.handleLogin());
        document.getElementById('logout-btn')?.addEventListener('click', () => this.handleLogout());
        document.getElementById('search-accounts')?.addEventListener('input', (e) => this.handleSearch(e));
        document.getElementById('refresh-btn')?.addEventListener('click', () => this.handleRefresh());
    }

    async handleLogin() {
        const email = document.getElementById('email')?.value;
        const password = document.getElementById('password')?.value;

        if (!email || !password) {
            ui.showError('Please enter email and password');
            return;
        }

        try {
            const data = await apiService.login(email, password);
            await storage.set('token', data.access_token);
            await this.initializeAccountManager();
            ui.showSuccess('Login successful');
        } catch (error) {
            ui.showError('Login failed. Please check your credentials.');
        }
    }

    async handleLogout() {
        await storage.remove(['token', 'currentAccount']);
        ui.showLoginForm();
    }

    handleSearch(event) {
        ui.filterAccounts(event.target.value);
    }

    async handleRefresh() {
        await this.loadAccounts();
    }

    async initializeAccountManager() {
        ui.showAccountManager();
        await this.loadAccounts();
    }

    async loadAccounts() {
        try {
            const accounts = await apiService.getAccounts();
            const currentAccount = await storage.get('currentAccount');
            ui.updateAccountsList(accounts, currentAccount);
        } catch (error) {
            if (error.message === 'unauthorized') {
                await this.handleLogout();
            } else {
                ui.showError('Failed to load accounts. Please try again.');
            }
        }
    }
}

const popupManager = new PopupManager();
document.addEventListener('DOMContentLoaded', () => popupManager.init());