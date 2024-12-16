import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { Account } from '../types';

export function useAccounts() {
  const queryClient = useQueryClient();

  const { data: accounts = [], isLoading } = useQuery({
    queryKey: ['accounts'],
    queryFn: async () => {
      const { data } = await api.get<Account[]>('/api/accounts');
      return data;
    }
  });

  const createAccount = useMutation({
    mutationFn: (newAccount: Partial<Account>) => 
      api.post('/api/accounts', newAccount),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
    }
  });

  const updateAccount = useMutation({
    mutationFn: ({ id, ...data }: Partial<Account> & { id: number }) =>
      api.put(`/api/accounts/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
    }
  });

  const deleteAccount = useMutation({
    mutationFn: (id: number) => api.delete(`/api/accounts/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
    }
  });

  return {
    accounts,
    isLoading,
    createAccount,
    updateAccount,
    deleteAccount
  };
}