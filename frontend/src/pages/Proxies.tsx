import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { Proxy } from '../types';
import { toast } from 'react-toastify';

export default function Proxies() {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);

  const { data: proxies = [], isLoading } = useQuery({
    queryKey: ['proxies'],
    queryFn: async () => {
      const { data } = await api.get<Proxy[]>('/api/proxies');
      return data;
    }
  });

  const createProxy = useMutation({
    mutationFn: (proxyData: Partial<Proxy>) => 
      api.post('/api/proxies', proxyData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['proxies'] });
      setShowForm(false);
      toast.success('Proxy created successfully');
    }
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-base font-semibold leading-6 text-gray-900">Proxies</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all proxy servers available in the system.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            onClick={() => setShowForm(true)}
            className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
          >
            Add proxy
          </button>
        </div>
      </div>

      <div className="mt-8 flow-root">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-300">
            <thead>
              <tr>
                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Host</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Port</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Type</th>
                <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-0">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {proxies.map((proxy) => (
                <tr key={proxy.id}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">{proxy.host}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{proxy.port}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{proxy.type}</td>
                  <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                    <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
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