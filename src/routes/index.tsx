import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Layout from '../components/Layout';
import Login from '../pages/Login';
import Accounts from '../pages/Accounts';
import Users from '../pages/Users';
import Analytics from '../pages/Analytics';
import Proxies from '../pages/Proxies';

function PrivateRoute({ children, adminOnly = false }: { children: React.ReactNode; adminOnly?: boolean }) {
  const { isAuthenticated, isAdmin } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (adminOnly && !isAdmin) {
    return <Navigate to="/accounts" />;
  }

  return <Layout>{children}</Layout>;
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/accounts" element={
        <PrivateRoute>
          <Accounts />
        </PrivateRoute>
      } />
      <Route path="/users" element={
        <PrivateRoute adminOnly>
          <Users />
        </PrivateRoute>
      } />
      <Route path="/analytics" element={
        <PrivateRoute adminOnly>
          <Analytics />
        </PrivateRoute>
      } />
      <Route path="/proxies" element={
        <PrivateRoute>
          <Proxies />
        </PrivateRoute>
      } />
      <Route path="/" element={<Navigate to="/accounts" />} />
    </Routes>
  );
}