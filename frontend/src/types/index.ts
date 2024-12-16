export interface User {
  email: string;
  is_admin: boolean;
  created_at: string;
  assigned_accounts: number[];
}

export interface Account {
  id: number;
  name: string;
  group?: string;
  group_id?: number;
  cookies: Cookie[];
  max_concurrent_users: number;
  active_sessions: number;
  active_users: ActiveUser[];
}

export interface Cookie {
  domain: string;
  name: string;
  value: string;
  path: string;
}

export interface ActiveUser {
  user_id: string;
  sessions: number;
  last_activity: string;
}

export interface Group {
  id: number;
  name: string;
  description?: string;
  accounts: Account[];
}

export interface Proxy {
  id: number;
  host: string;
  port: number;
  username?: string;
  password?: string;
  type: 'https' | 'socks5';
}

export interface Analytics {
  total_sessions: number;
  active_accounts: number;
  active_users: number;
  recent_activity: ActivityLog[];
}

export interface ActivityLog {
  user_id: string;
  account_id: number;
  domain: string;
  timestamp: string;
  action: string;
}