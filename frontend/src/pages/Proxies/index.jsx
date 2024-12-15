import { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { getAuthHeader } from '../../api/auth';

export default function Proxies() {
  const [proxies, setProxies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProxies();
  }, []);

  const loadProxies = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/proxies`, {
        headers: getAuthHeader()
      });
      setProxies(response.data);
    } catch (error) {
      toast.error('Failed to load proxies');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Proxies</h2>
      <div className="bg-white shadow rounded-lg">
        <table className="min-w-full">
          <thead>
            <tr>
              <th className="px-6 py-3 border-b text-left">Host</th>
              <th className="px-6 py-3 border-b text-left">Port</th>
              <th className="px-6 py-3 border-b text-left">Type</th>
              <th className="px-6 py-3 border-b text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {proxies.map((proxy) => (
              <tr key={proxy.id}>
                <td className="px-6 py-4">{proxy.host}</td>
                <td className="px-6 py-4">{proxy.port}</td>
                <td className="px-6 py-4">{proxy.type}</td>
                <td className="px-6 py-4">
                  <button className="text-red-500 hover:text-red-700">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}