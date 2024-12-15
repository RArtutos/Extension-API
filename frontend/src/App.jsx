import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Layout from './components/Layout';
import PrivateRoute from './components/PrivateRoute';
import Login from './pages/Login';
import Accounts from './pages/Accounts';
import Proxies from './pages/Proxies';

export default function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route index element={<Accounts />} />
            <Route path="proxies" element={<Proxies />} />
          </Route>
        </Routes>
      </Router>
      <ToastContainer />
    </>
  );
}