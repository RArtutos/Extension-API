export class TabManager {
  async hasOpenTabsForAccount(account) {
    try {
      const tabs = await chrome.tabs.query({});
      return tabs.some((tab) => {
        try {
          if (!tab.url) return false;
          const domain = new URL(tab.url).hostname;
          return account.cookies.some((cookie) =>
            domain.endsWith(cookie.domain.replace(/^\./, ''))
          );
        } catch {
          return false;
        }
      });
    } catch (error) {
      console.error('Error checking open tabs:', error);
      return false;
    }
  }
}