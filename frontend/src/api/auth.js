import axios from 'axios';

const API_URL = 'http://84.46.249.121:3000/api';

export const login = async (credentials) => {
  const response = await axios.post(`${API_URL}/auth/login`, credentials);
  return response.data;
};

export const register = async (userData) => {
  const response = await axios.post(`${API_URL}/auth/register`, userData);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
};