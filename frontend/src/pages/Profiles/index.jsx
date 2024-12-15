import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import ProfileList from './components/ProfileList';
import ProfileForm from './components/ProfileForm';
import { getProfiles } from '../../api/profiles';

export default function Profiles() {
  const [isCreating, setIsCreating] = useState(false);
  const { data: profiles, isLoading } = useQuery(['profiles'], getProfiles);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Profiles</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-500 text-white px-4 py-2 rounded-md"
        >
          Create Profile
        </button>
      </div>

      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <ProfileList profiles={profiles} />
      )}

      {isCreating && (
        <ProfileForm onClose={() => setIsCreating(false)} />
      )}
    </div>
  );
}