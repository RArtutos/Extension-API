import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import ProxyList from './components/ProxyList';
import ProxyForm from './components/ProxyForm';
import { getProxies } from '../../api/proxies';

export default function Proxies() {
  const [isCreating, setIsCreating] = useState(false);
  const { data: proxies, isLoading } = useQuery(['proxies'], getProxies);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Proxies</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-500 text-white px-4 py-2 rounded-md"
        >
          Add Proxy
        </button>
      </div>

      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <ProxyList proxies={proxies} />
      )}

      {isCreating && (
        <ProxyForm onClose={() => setIsCreating(false)} />
      )}
    </div>
  );
}