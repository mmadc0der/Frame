import React from 'react';
import { render, screen, act } from '@testing-library/react';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import { describe, it, expect, vi } from 'vitest';

const TestComponent: React.FC = () => {
  const { accessToken, isAuthenticated, setAccessToken, clearTokens } = useAuth();

  return (
    <div>
      <span data-testid="access-token">{accessToken || 'null'}</span>
      <span data-testid="is-authenticated">{isAuthenticated ? 'true' : 'false'}</span>
      <button onClick={() => setAccessToken('test-token')}>Set Token</button>
      <button onClick={clearTokens}>Clear Tokens</button>
    </div>
  );
};

describe('AuthContext', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });
  
  it('should initialize with null accessToken and isAuthenticated as false', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByTestId('access-token').textContent).toBe('null');
    expect(screen.getByTestId('is-authenticated').textContent).toBe('false');
  });

  it('should update accessToken when setAccessToken is called', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    const setTokenButton = screen.getByText('Set Token');

    act(() => {
      setTokenButton.click();
    });

    expect(screen.getByTestId('access-token').textContent).toBe('test-token');
    expect(screen.getByTestId('is-authenticated').textContent).toBe('true');
  });

  it('should clear accessToken when clearTokens is called', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    const setTokenButton = screen.getByText('Set Token');
    const clearTokensButton = screen.getByText('Clear Tokens');

    // Устанавливаем токен
    act(() => {
      setTokenButton.click();
    });

    // Проверяем, что токен установлен
    expect(screen.getByTestId('access-token').textContent).toBe('test-token');
    expect(screen.getByTestId('is-authenticated').textContent).toBe('true');

    // Очищаем токен
    act(() => {
      clearTokensButton.click();
    });

    // Проверяем, что токен очищен
    expect(screen.getByTestId('access-token').textContent).toBe('null');
    expect(screen.getByTestId('is-authenticated').textContent).toBe('false');
  });
});
