import { api, handleApiError } from './api';
import { LoginRequest, RegisterRequest, LoginResponse, RegisterResponse } from '../types/api';
import { useAuth } from '../contexts/AuthContext';

export const authService = {
  async register(data: RegisterRequest): Promise<RegisterResponse> {
    try {
      const response = await api.post<RegisterResponse>('/auth/register', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async login(data: LoginRequest): Promise<void> {
    try {
      const response = await api.post<LoginResponse>('/auth/login', data);
      const { access_token } = response.data;

      const auth = useAuth();

      // Устанавливаем Access-токен в AuthContext
      auth.setAccessToken(access_token);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout'); // Если есть logout endpoint на сервере
    } catch (error) {
      console.warn('Logout request failed, proceeding with local logout:', handleApiError(error));
    }

    const auth = useAuth();

    // Очищаем токены в AuthContext
    auth.clearTokens();

    // Перенаправление на страницу входа
    window.location.href = '/login';
  },

  isAuthenticated(): boolean {
    const auth = useAuth();
    return auth.isAuthenticated;
  },
};
