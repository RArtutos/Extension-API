import { api } from '../utils/api.js';
import { storage } from '../utils/storage.js';
import { cookieService } from './cookieService.js';
import { analyticsService } from './analyticsService.js';

class AccountService {
    async switchAccount(account) {
        try {
            // Check session limit
            const sessionInfo = await api.getSessionInfo(account.id);
            if (sessionInfo.active_sessions >= sessionInfo.max_concurrent_users) {
                throw new Error(`Maximum concurrent users (${sessionInfo.max_concurrent_users}) reached`);
            }

            const currentAccount = await this.getCurrentAccount();
            
            // Remove old cookies and log out
            if (currentAccount) {
                await cookieService.removeAccountCookies(currentAccount);
                await analyticsService.logAccess(currentAccount.id, 'logout');
            }

            // Set new cookies and log in
            await cookieService.setAccountCookies(account);
            await storage.set('currentAccount', account);
            await analyticsService.logAccess(account.id, 'login');

            // Start monitoring domain activity
            if (account.cookies) {
                for (const cookie of account.cookies) {
                    analyticsService.startDomainTimer(cookie.domain);
                }
            }

            return account;
        } catch (error) {
            console.error('Error switching account:', error);
            throw error;
        }
    }

    // [Previous methods remain unchanged]
}

export const accountService = new AccountService();