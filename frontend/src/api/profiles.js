import axios from 'axios';
import { getAuthHeader } from '../utils/auth';

const API_URL = 'http://localhost:3000/api';

export const getProfiles = async () => {
  const response = await axios.get(`${API_URL}/profiles`, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const createProfile = async (profileData) => {
  const response = await axios.post(`${API_URL}/profiles`, profileData, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const updateProfile = async ({ id, ...profileData }) => {
  const response = await axios.put(`${API_URL}/profiles/${id}`, profileData, {
    headers: getAuthHeader(),
  });
  return response.data;
};

export const deleteProfile = async (id) => {
  const response = await axios.delete(`${API_URL}/profiles/${id}`, {
    headers: getAuthHeader(),
  });
  return response.data;
};