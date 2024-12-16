import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useAccounts } from '../../hooks/useAccounts';
import { useGroups } from '../../hooks/useGroups';
import { toast } from 'react-toastify';

interface AccountFormData {
  name: string;
  group?: number;
  domain: string;
  cookies: string;
  max_concurrent_users: number;
}

export default function AccountForm() {
  const navigate = useNavigate();
  const { createAccount } = useAccounts();
  const { groups } = useGroups();
  const { register, handleSubmit, formState: { errors } } = useForm<AccountFormData>();

  const onSubmit = async (data: AccountFormData) => {
    try {
      const cookies = [{
        domain: data.domain,
        name: 'header_cookies',
        value: data.cookies,
        path: '/'
      }];

      await createAccount.mutateAsync({
        name: data.name,
        group: data.group,
        cookies,
        max_concurrent_users: data.max_concurrent_users
      });

      toast.success('Account created successfully');
      navigate('/accounts');
    } catch (error) {
      toast.error('Failed to create account');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Name
        </label>
        <input
          type="text"
          {...register('name', { required: true })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
        {errors.name && <span className="text-red-500 text-sm">Name is required</span>}
      </div>

      <div>
        <label htmlFor="group" className="block text-sm font-medium text-gray-700">
          Group
        </label>
        <select
          {...register('group')}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        >
          <option value="">Select a group</option>
          {groups.map(group => (
            <option key={group.id} value={group.id}>{group.name}</option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="domain" className="block text-sm font-medium text-gray-700">
          Domain
        </label>
        <input
          type="text"
          {...register('domain', { required: true })}
          placeholder=".example.com"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
        {errors.domain && <span className="text-red-500 text-sm">Domain is required</span>}
      </div>

      <div>
        <label htmlFor="cookies" className="block text-sm font-medium text-gray-700">
          Cookies
        </label>
        <textarea
          {...register('cookies', { required: true })}
          rows={4}
          placeholder="name1=value1; name2=value2"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
        {errors.cookies && <span className="text-red-500 text-sm">Cookies are required</span>}
      </div>

      <div>
        <label htmlFor="max_concurrent_users" className="block text-sm font-medium text-gray-700">
          Maximum Concurrent Users
        </label>
        <input
          type="number"
          {...register('max_concurrent_users', { required: true, min: 1 })}
          defaultValue={1}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <div className="flex justify-end gap-3">
        <button
          type="button"
          onClick={() => navigate('/accounts')}
          className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700"
        >
          Create Account
        </button>
      </div>
    </form>
  );
}