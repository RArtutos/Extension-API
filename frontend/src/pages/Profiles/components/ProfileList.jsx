import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { deleteProfile } from '../../../api/profiles';
import ProfileDetails from './ProfileDetails';

export default function ProfileList({ profiles }) {
  const [selectedProfile, setSelectedProfile] = useState(null);
  const queryClient = useQueryClient();

  const deleteMutation = useMutation(deleteProfile, {
    onSuccess: () => {
      queryClient.invalidateQueries(['profiles']);
    },
  });

  return (
    <div className="bg-white rounded-lg shadow">
      <table className="min-w-full">
        <thead>
          <tr>
            <th className="px-6 py-3 border-b">Name</th>
            <th className="px-6 py-3 border-b">Cookies</th>
            <th className="px-6 py-3 border-b">Proxy</th>
            <th className="px-6 py-3 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {profiles.map((profile) => (
            <tr key={profile.id}>
              <td className="px-6 py-4">{profile.name}</td>
              <td className="px-6 py-4">{profile.cookies.length} cookies</td>
              <td className="px-6 py-4">
                {profile.proxy ? profile.proxy.host : 'None'}
              </td>
              <td className="px-6 py-4">
                <button
                  onClick={() => setSelectedProfile(profile)}
                  className="text-blue-500 hover:text-blue-700 mr-2"
                >
                  Edit
                </button>
                <button
                  onClick={() => deleteMutation.mutate(profile.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedProfile && (
        <ProfileDetails
          profile={selectedProfile}
          onClose={() => setSelectedProfile(null)}
        />
      )}
    </div>
  );
}