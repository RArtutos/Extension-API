export function getAccountDomain(account) {
  if (!account?.cookies?.length) return '';
  const domain = account.cookies[0].domain;
  return domain.startsWith('.') ? domain.substring(1) : domain;
}

export function isTabForAccount(tab, account) {
  try {
    if (!tab.url) return false;
    const domain = new URL(tab.url).hostname;
    return account.cookies.some(cookie => 
      domain.endsWith(cookie.domain.replace(/^\./, ''))
    );
  } catch {
    return false;
  }
}