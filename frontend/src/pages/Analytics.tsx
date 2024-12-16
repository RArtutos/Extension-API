import { useAnalytics } from '../hooks/useAnalytics';

export default function Analytics() {
  const { data: analytics, isLoading } = useAnalytics();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Analytics Dashboard</h1>
      
      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
          <dt className="truncate text-sm font-medium text-gray-500">Total Sessions</dt>
          <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
            {analytics?.total_sessions || 0}
          </dd>
        </div>
        <div className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
          <dt className="truncate text-sm font-medium text-gray-500">Active Accounts</dt>
          <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
            {analytics?.active_accounts || 0}
          </dd>
        </div>
        <div className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
          <dt className="truncate text-sm font-medium text-gray-500">Active Users</dt>
          <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
            {analytics?.active_users || 0}
          </dd>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-lg font-medium text-gray-900">Recent Activity</h2>
        <div className="mt-4 overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">User</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Account</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Domain</th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {analytics?.recent_activity.map((activity, idx) => (
                <tr key={idx}>
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm text-gray-900">{activity.user_id}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{activity.account_id}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{activity.domain}</td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {new Date(activity.timestamp).toLocaleString()}
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