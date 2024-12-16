import { useUsers } from '../../hooks/useUsers';
import { toast } from 'react-toastify';

export default function UserList() {
  const { users, isLoading, deleteUser } = useUsers();

  const handleDelete = async (email: string) => {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
      await deleteUser.mutateAsync(email);
      toast.success('User deleted successfully');
    } catch (error) {
      toast.error('Failed to delete user');
    }
  };

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="mt-8 flow-root">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-300">
          <thead>
            <tr>
              <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">
                Email
              </th>
              <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                Role
              </th>
              <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                Assigned Accounts
              </th>
              <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-0">
                <span className="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {users.map((user) => (
              <tr key={user.email}>
                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">
                  {user.email}
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                  {user.is_admin ? 'Admin' : 'User'}
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                  {user.assigned_accounts.length}
                </td>
                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                  <button
                    onClick={() => handleDelete(user.email)}
                    className="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}