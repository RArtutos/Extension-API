import axios from 'axios';
import { getAuthHeader } from '../utils/auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getFolders = async () => {
  const response = await axios.get(`${API_URL}/api/folders`, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const createFolder = async (folderData) => {
  const response = await axios.post(`${API_URL}/api/folders`, folderData, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const deleteFolder = async (id) => {
  const response = await axios.delete(`${API_URL}/api/folders/${id}`, {
    headers: getAuthHeader(),
  });
  return response.data;
};