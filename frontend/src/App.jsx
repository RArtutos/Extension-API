import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Layout from './components/Layout';
import PrivateRoute from './components/PrivateRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Profiles from './pages/Profiles';
import Folders from './pages/Folders';
import Proxies from './pages/Proxies';
import Settings from './pages/Settings';

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route index element={<Dashboard />} />
            <Route path="profiles" element={<Profiles />} />
            <Route path="folders" element={<Folders />} />
            <Route path="proxies" element={<Proxies />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </Router>
      <ToastContainer />
    </QueryClientProvider>
  );
}