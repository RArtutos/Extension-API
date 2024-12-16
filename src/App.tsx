import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastContainer } from 'react-toastify';
import AppRoutes from './routes';
import { AuthProvider } from './contexts/AuthContext';
import 'react-toastify/dist/ReactToastify.css';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <AppRoutes />
          <ToastContainer position="top-right" />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;