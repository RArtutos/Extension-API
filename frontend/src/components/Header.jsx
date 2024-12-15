import { useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

export default function Header() {
  const navigate = useNavigate();
  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-white shadow">
      <div className="px-4 py-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Cookie Manager</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
        >
          Logout
        </button>
      </div>
    </header>
  );
}