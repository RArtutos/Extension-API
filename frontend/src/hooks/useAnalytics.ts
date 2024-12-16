import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { Analytics } from '../types';

export function useAnalytics() {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: async () => {
      const { data } = await api.get<Analytics>('/api/admin/analytics');
      return data;
    },
    refetchInterval: 30000 // Refresh every 30 seconds
  });
}