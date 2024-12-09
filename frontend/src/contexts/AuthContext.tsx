import React, { createContext, useState, useContext, ReactNode } from 'react';

interface AuthContextType {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
  clearTokens: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [accessToken, setAccessToken] = useState<string | null>(null);

  const clearTokens = () => {
    setAccessToken(null); // Очищаем Access-токен
  };

  const isAuthenticated = !!accessToken;

  return (
    <AuthContext.Provider value={{ 
      accessToken, 
      setAccessToken, 
      clearTokens, 
      isAuthenticated 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
