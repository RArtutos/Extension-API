import axios from 'axios';
import { getAuthHeader } from '../utils/auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const getProfiles = async () => {
  const response = await axios.get(`${API_URL}/api/profiles`, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const createProfile = async (profileData) => {
  const response = await axios.post(`${API_URL}/api/profiles`, profileData, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const updateProfile = async ({ id, ...profileData }) => {
  const response = await axios.put(`${API_URL}/api/profiles/${id}`, profileData, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const deleteProfile = async (id) => {
  const response = await axios.delete(`${API_URL}/api/profiles/${id}`, {
    headers: getAuthHeader(),
  });
  return response.data;
};