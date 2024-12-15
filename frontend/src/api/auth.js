import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export const login = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/api/auth/login`, {
      username: credentials.email,  // FastAPI espera 'username' en lugar de 'email'
      password: credentials.password
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error de login:', error);
    throw error;
  }
};

export const register = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/api/auth/register`, {
      username: userData.email,
      password: userData.password
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error de registro:', error);
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('token');
};