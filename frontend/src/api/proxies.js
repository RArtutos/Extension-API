import axios from 'axios';
import { getAuthHeader } from '../utils/auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getProxies = async () => {
  const response = await axios.get(`${API_URL}/api/proxies`, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const createProxy = async (proxyData) => {
  const response = await axios.post(`${API_URL}/api/proxies`, proxyData, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const deleteProxy = async (id) => {
  const response = await axios.delete(`${API_URL}/api/proxies/${id}`, {
    headers: getAuthHeader(),
  });
  return response.data;
};