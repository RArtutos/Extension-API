import { storage } from './utils/storage.js';
import { apiService } from './services/api.service.js';
import { ui } from './utils/ui.js';
import { accountManager } from './accountManager.js';
import { STORAGE_KEYS } from './config.js';

class PopupManager {
    constructor() {
        this.initialized = false;
        this.bindEventHandlers();
    }

    bindEventHandlers() {
        this.handleLogin = this.handleLogin.bind(this);
        this.handleLogout = this.handleLogout.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
        this.handleRefresh = this.handleRefresh.bind(this);
    }

    attachEventListeners() {
        document.getElementById('login-btn')?.addEventListener('click', this.handleLogin);
        document.getElementById('logout-btn')?.addEventListener('click', this.handleLogout);
        document.getElementById('search-accounts')?.addEventListener('input', this.handleSearch);
        document.getElementById('refresh-btn')?.addEventListener('click', this.handleRefresh);
    }

    async init() {
        if (this.initialized) return;
        await this.checkAuthState();
        this.attachEventListeners();
        this.initialized = true;
    }

    async checkAuthState() {
        const token = await storage.get(STORAGE_KEYS.TOKEN);
        if (token) {
            try {
                const userData = await apiService.validateToken(token);
                if (userData) {
                    await this.initializeAccountManager();
                    return;
                }
            } catch (error) {
                console.error('Token validation failed:', error);
                await storage.remove(STORAGE_KEYS.TOKEN);
            }
        }
        ui.showLoginForm();
    }

    async handleLogin() {
        const email = document.getElementById('email')?.value;
        const password = document.getElementById('password')?.value;

        if (!email || !password) {
            ui.showError('Please enter email and password');
            return;
        }

        try {
            await apiService.login(email, password);
            await this.initializeAccountManager();
            ui.showSuccess('Login successful');
        } catch (error) {
            console.error('Login failed:', error);
            ui.showError('Login failed. Please check your credentials.');
        }
    }

    async handleLogout() {
        await storage.remove([STORAGE_KEYS.TOKEN, STORAGE_KEYS.CURRENT_ACCOUNT]);
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
        await accountManager.init();
    }

    async loadAccounts() {
        try {
            const accounts = await apiService.getAccounts();
            const currentAccount = await storage.get(STORAGE_KEYS.CURRENT_ACCOUNT);
            ui.updateAccountsList(accounts, currentAccount);
        } catch (error) {
            console.error('Failed to load accounts:', error);
            if (error.message === 'unauthorized') {
                await this.handleLogout();
            } else {
                ui.showError('Failed to load accounts');
            }
        }
    }
}

// Initialize popup
const popupManager = new PopupManager();
document.addEventListener('DOMContentLoaded', () => popupManager.init());