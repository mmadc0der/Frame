import axios, { AxiosError } from 'axios';
import { ApiError } from '../types/api';
import { useAuth } from '../contexts/AuthContext';

//const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/';

const BASE_URL = 'http://localhost:5000/';

declare module 'axios' {
  export interface InternalAxiosRequestConfig<D = any> extends AxiosRequestConfig {
    _retry?: boolean;
  }
}

export const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Передача cookies с запросами
});

// Перехватчик запросов для добавления токена авторизации
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config;

    // Проверяем, что это 401 ошибка, и запрос еще не повторялся
    if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true; // Помечаем запрос, чтобы избежать циклов

      try {
        // Пытаемся обновить токен
        const response = await axios.post(`${BASE_URL}/auth/refresh`, null, {
          withCredentials: true, // Refresh-токен передается через cookies
        });

        const { accessToken } = response.data;
        const auth = useAuth();

        auth.setAccessToken(accessToken); // Сохраняем новый Access-токен в контексте

        // Повторяем оригинальный запрос с обновленным токеном
        originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        const auth = useAuth();

        // Если обновление токена не удалось, очищаем состояние и перенаправляем
        auth.clearTokens();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const apiError = error.response?.data as ApiError;
    return apiError?.error?.message || 'An unexpected error occurred';
  }
  return 'An unexpected error occurred';
};
