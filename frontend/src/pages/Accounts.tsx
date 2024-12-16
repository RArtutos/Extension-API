import { Link } from 'react-router-dom';
import AccountList from '../components/Accounts/AccountList';

export default function Accounts() {
  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-base font-semibold leading-6 text-gray-900">Accounts</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all accounts including their name, group, and active sessions.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <Link
            to="/accounts/new"
            className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Add account
          </Link>
        </div>
      </div>
      <AccountList />
    </div>
  );
}