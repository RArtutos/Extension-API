import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { User } from '../types';

export function useUsers() {
  const queryClient = useQueryClient();

  const { data: users = [], isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await api.get<User[]>('/api/admin/users');
      return data;
    }
  });

  const createUser = useMutation({
    mutationFn: (userData: Partial<User>) => 
      api.post('/api/admin/users', userData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });

  const deleteUser = useMutation({
    mutationFn: (email: string) => 
      api.delete(`/api/admin/users/${email}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });

  return {
    users,
    isLoading,
    createUser,
    deleteUser
  };
}