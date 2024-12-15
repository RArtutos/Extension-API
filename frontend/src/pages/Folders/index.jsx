import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import FolderList from './components/FolderList';
import FolderForm from './components/FolderForm';
import { getFolders } from '../../api/folders';

export default function Folders() {
  const [isCreating, setIsCreating] = useState(false);
  const { data: folders, isLoading } = useQuery(['folders'], getFolders);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Folders</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-500 text-white px-4 py-2 rounded-md"
        >
          Create Folder
        </button>
      </div>

      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <FolderList folders={folders} />
      )}

      {isCreating && (
        <FolderForm onClose={() => setIsCreating(false)} />
      )}
    </div>
  );
}