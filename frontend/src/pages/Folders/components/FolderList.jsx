import { useMutation, useQueryClient } from '@tanstack/react-query';
import { deleteFolder } from '../../../api/folders';

export default function FolderList({ folders }) {
  const queryClient = useQueryClient();

  const deleteMutation = useMutation(deleteFolder, {
    onSuccess: () => {
      queryClient.invalidateQueries(['folders']);
    },
  });

  return (
    <div className="bg-white rounded-lg shadow">
      <table className="min-w-full">
        <thead>
          <tr>
            <th className="px-6 py-3 border-b">Name</th>
            <th className="px-6 py-3 border-b">Profiles</th>
            <th className="px-6 py-3 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {folders?.map((folder) => (
            <tr key={folder.id}>
              <td className="px-6 py-4">{folder.name}</td>
              <td className="px-6 py-4">{folder.profiles?.length || 0} profiles</td>
              <td className="px-6 py-4">
                <button
                  onClick={() => deleteMutation.mutate(folder.id)}
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