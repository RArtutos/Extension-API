import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  return (
    <div className="fixed w-64 h-full bg-gray-800">
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-center h-16 bg-gray-900">
          <span className="text-white text-xl font-semibold">Account Manager</span>
        </div>
        <nav className="flex-1 px-2 py-4">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `flex items-center px-4 py-2 mt-2 text-gray-100 rounded-lg hover:bg-gray-700 ${
                isActive ? 'bg-gray-700' : ''
              }`
            }
          >
            Accounts
          </NavLink>
          <NavLink
            to="/proxies"
            className={({ isActive }) =>
              `flex items-center px-4 py-2 mt-2 text-gray-100 rounded-lg hover:bg-gray-700 ${
                isActive ? 'bg-gray-700' : ''
              }`
            }
          >
            Proxies
          </NavLink>
        </nav>
      </div>
    </div>
  );
}