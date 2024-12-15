import { useMutation, useQueryClient } from '@tanstack/react-query';
import { deleteProxy } from '../../../api/proxies';

export default function ProxyList({ proxies }) {
  const queryClient = useQueryClient();

  const deleteMutation = useMutation(deleteProxy, {
    onSuccess: () => {
      queryClient.invalidateQueries(['proxies']);
    },
  });

  return (
    <div className="bg-white rounded-lg shadow">
      <table className="min-w-full">
        <thead>
          <tr>
            <th className="px-6 py-3 border-b">Host</th>
            <th className="px-6 py-3 border-b">Port</th>
            <th className="px-6 py-3 border-b">Username</th>
            <th className="px-6 py-3 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {proxies?.map((proxy) => (
            <tr key={proxy.id}>
              <td className="px-6 py-4">{proxy.host}</td>
              <td className="px-6 py-4">{proxy.port}</td>
              <td className="px-6 py-4">{proxy.username || '-'}</td>
              <td className="px-6 py-4">
                <button
                  onClick={() => deleteMutation.mutate(proxy.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}