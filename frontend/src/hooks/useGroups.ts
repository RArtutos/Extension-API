import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { Group } from '../types';

export function useGroups() {
  const queryClient = useQueryClient();

  const { data: groups = [], isLoading } = useQuery({
    queryKey: ['groups'],
    queryFn: async () => {
      const { data } = await api.get<Group[]>('/api/groups');
      return data;
    }
  });

  const createGroup = useMutation({
    mutationFn: (newGroup: Partial<Group>) => 
      api.post('/api/groups', newGroup),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] });
    }
  });

  const assignAccount = useMutation({
    mutationFn: ({ groupId, accountId }: { groupId: number; accountId: number }) =>
      api.post(`/api/groups/${groupId}/accounts/${accountId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] });
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
    }
  });

  return {
    groups,
    isLoading,
    createGroup,
    assignAccount
  };
}