import { storage } from './utils/storage.js';
import { api } from './utils/api.js';
import { ui } from './utils/ui.js';
import { accountManager } from './accountManager.js';

class PopupManager {
    constructor() {
        this.initialized = false;
    }

    async init() {
        if (this.initialized) return;
        
        // Verificar estado de autenticación
        const token = await storage.get('token');
        if (!token) {
            ui.showLoginForm();
        } else {
            await this.initializeAccountManager();
        }

        this.attachEventListeners();
        this.initialized = true;
    }

    attachEventListeners() {
        // Login
        document.getElementById('login-btn')?.addEventListener('click', async () => {
            const email = document.getElementById('email')?.value;
            const password = document.getElementById('password')?.value;

            if (!email || !password) {
                ui.showError('Por favor ingrese email y contraseña');
                return;
            }

            try {
                const data = await api.login(email, password);
                if (data.access_token) {
                    await storage.set('token', data.access_token);
                    await this.initializeAccountManager();
                    ui.showSuccess('Inicio de sesión exitoso');
                }
            } catch (error) {
                console.error('Error de inicio de sesión:', error);
                ui.showError('Error al iniciar sesión. Verifique sus credenciales.');
            }
        });

        // Logout
        document.getElementById('logout-btn')?.addEventListener('click', async () => {
            await storage.remove(['token', 'currentAccount']);
            ui.showLoginForm();
        });

        // Búsqueda de cuentas
        document.getElementById('search-accounts')?.addEventListener('input', (e) => {
            ui.filterAccounts(e.target.value);
        });

        // Refresh
        document.getElementById('refresh-btn')?.addEventListener('click', () => {
            accountManager.loadAccounts();
        });
    }

    async initializeAccountManager() {
        ui.showAccountManager();
        await accountManager.init();
    }
}

// Inicializar popup
const popupManager = new PopupManager();
document.addEventListener('DOMContentLoaded', () => popupManager.init());