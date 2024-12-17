export interface ApiError {
  error: {
    code: string;
    message: string;
  };
}

export interface RegisterRequest {
  email: string;
  password: string;
  // username: string;
}

export interface RegisterResponse {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: RegisterResponse | null;
  tokens: {
    access: string | null;
    refresh: string | null;
  };
}
