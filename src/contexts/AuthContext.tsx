import { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

interface AuthContextType {
  user: any;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // TODO: Validate token and get user info
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await api.post('/api/auth/login', {
        username: email,
        password,
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      setUser({ email, isAdmin: email === 'admin@artutos.eu.org' });
      navigate('/accounts');
    } catch (error) {
      throw new Error('Invalid credentials');
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      isAuthenticated: !!user,
      isAdmin: user?.isAdmin || false,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}