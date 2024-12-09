import { api, handleApiError } from './api';
import { LoginRequest, RegisterRequest, LoginResponse, RegisterResponse } from '../types/api';
import { useAuth } from '../contexts/AuthContext';

export const authService = {
  async login(data: LoginRequest): Promise<void> {
    try {
      const response = await api.post<LoginResponse>('/auth/login', data);
      const { access_token } = response.data;

      const auth = useAuth();
      auth.setAccessToken(access_token);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async register(data: RegisterRequest): Promise<RegisterResponse> {
    try {
      const response = await api.post<RegisterResponse>('/auth/register', data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async loginWithYandex(): Promise<void> {
    const clientId = import.meta.env.VITE_YANDEX_CLIENT_ID;
    const redirectUri = `${window.location.origin}/auth/yandex/callback`;
    const scope = 'login:info login:email';
    
    //TODO: finish registration of application in yandex, after receiving domain
    const authUrl = `https://oauth.yandex.ru/authorize?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}`;
    
    window.location.href = authUrl;
  },

  async handleYandexCallback(code: string): Promise<void> {
    try {
      const response = await api.post<LoginResponse>('/auth/yandex/callback', { code });
      const { access_token } = response.data;

      const auth = useAuth();
      auth.setAccessToken(access_token);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  async loginWithGitHub(): Promise<void> {
    const clientId = import.meta.env.VITE_GITHUB_CLIENT_ID;
    const redirectUri = `${window.location.origin}/auth/github/callback`;
    const scope = 'user:email';
    
    const authUrl = `https://github.com/login/oauth/authorize?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}`;
    
    window.location.href = authUrl;
  },

  async handleGitHubCallback(code: string): Promise<void> {
    try {
      const response = await api.post<LoginResponse>('/auth/github/callback', { code });
      const { access_token } = response.data;

      const auth = useAuth();
      auth.setAccessToken(access_token);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  isAuthenticated(): boolean {
    const auth = useAuth();
    return auth.isAuthenticated;
  },

  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.warn('Logout request failed, proceeding with local logout:', handleApiError(error));
    }

    const auth = useAuth();
    auth.clearTokens();
    window.location.href = '/login';
  }
};
