import { Account } from '../../types';
import { useAccounts } from '../../hooks/useAccounts';
import { useGroups } from '../../hooks/useGroups';
import { toast } from 'react-toastify';

export default function AccountList() {
  const { accounts, isLoading, deleteAccount } = useAccounts();
  const { groups, assignAccount } = useGroups();

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this account?')) return;
    
    try {
      await deleteAccount.mutateAsync(id);
      toast.success('Account deleted successfully');
    } catch (error) {
      toast.error('Failed to delete account');
    }
  };

  const handleAssignGroup = async (accountId: number, groupId: number) => {
    try {
      await assignAccount.mutateAsync({ accountId, groupId });
      toast.success('Account assigned to group');
    } catch (error) {
      toast.error('Failed to assign account to group');
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="mt-8 flow-root">
      <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <table className="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">
                  Name
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Group
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Sessions
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Active Users
                </th>
                <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-0">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {accounts.map((account) => (
                <tr key={account.id}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">
                    {account.name}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {account.group || '-'}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {account.active_sessions}/{account.max_concurrent_users}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {account.active_users.map(user => (
                      <div key={user.user_id}>
                        {user.user_id} ({user.sessions})
                      </div>
                    ))}
                  </td>
                  <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                    <button
                      onClick={() => handleDelete(account.id)}
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
    </div>
  );
}