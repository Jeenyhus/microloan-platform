import axios from 'axios';
import { LoginCredentials, RegisterData, AuthResponse } from '../types/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await axios.post(`${API_URL}/token/`, credentials);
    return response.data;
  },

  register: async (data: RegisterData) => {
    const response = await axios.post(`${API_URL}/register/`, data);
    return response.data;
  },

  refreshToken: async (refresh: string): Promise<AuthResponse> => {
    const response = await axios.post(`${API_URL}/token/refresh/`, { refresh });
    return response.data;
  },

  getUser: async (token: string) => {
    const response = await axios.get(`${API_URL}/users/me/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  }
}; 