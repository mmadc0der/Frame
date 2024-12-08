import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider } from 'styled-components';
import styled from 'styled-components';
import { LoginForm } from '../components/auth/LoginForm';
import { RegisterForm } from '../components/auth/RegisterForm';
import { theme } from '../styles/theme';

const SwitchText = styled.p`
  text-align: center;
  margin-top: 1rem;
  color: ${props => props.theme.colors.primary};
  font-size: 0.875rem;
`;

const SwitchLink = styled.button`
  background: none;
  border: none;
  color: ${props => props.theme.colors.accent};
  font-weight: 500;
  cursor: pointer;
  padding: 0;
  font-size: 0.875rem;
  text-decoration: underline;
  
  &:hover {
    color: ${props => props.theme.colors.primary};
  }
`;

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('Authentication Forms', () => {
  describe('LoginForm', () => {
    const mockSwitch = jest.fn();

    beforeEach(() => {
      renderWithTheme(<LoginForm onSwitch={mockSwitch} />);
    });

    it('renders login form correctly', () => {
      expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
      expect(screen.getByText('Log In')).toBeInTheDocument();
    });

    it('shows error for invalid email', async () => {
      const emailInput = screen.getByPlaceholderText('Email');

      fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
      fireEvent.blur(emailInput);

      await waitFor(() => {
        const errorMessage = screen.getByText('Email is invalid');
        expect(errorMessage).toBeInTheDocument();
      });
    });

    it('shows error for short password', async () => {
      const passwordInput = screen.getByPlaceholderText('Password');

      fireEvent.change(passwordInput, { target: { value: '123' } });
      fireEvent.blur(passwordInput);

      await waitFor(() => {
        const errorMessage = screen.getByText('Password must be at least 6 characters');
        expect(errorMessage).toBeInTheDocument();
      });
    });

    it('calls onSwitch when Sign Up link is clicked', () => {
      const switchLink = screen.getByText('Sign Up');
      fireEvent.click(switchLink);
      expect(mockSwitch).toHaveBeenCalled();
    });
  });

  describe('RegisterForm', () => {
    const mockSwitch = jest.fn();

    beforeEach(() => {
      renderWithTheme(<RegisterForm onSwitch={mockSwitch} />);
    });

    it('renders registration form correctly', () => {
      expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Confirm Password')).toBeInTheDocument();
      expect(screen.getByText('Sign Up')).toBeInTheDocument();
    });

    it('shows error when passwords do not match', async () => {
      const passwordInput = screen.getByPlaceholderText('Password');
      const confirmPasswordInput = screen.getByPlaceholderText('Confirm Password');

      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.change(confirmPasswordInput, { target: { value: 'differentpassword' } });
      fireEvent.blur(confirmPasswordInput);

      await waitFor(() => {
        const errorMessage = screen.getByText('Passwords do not match');
        expect(errorMessage).toBeInTheDocument();
      });
    });

    it('shows error for invalid email', async () => {
      const emailInput = screen.getByPlaceholderText('Email');

      fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
      fireEvent.blur(emailInput);

      await waitFor(() => {
        const errorMessage = screen.getByText('Email is invalid');
        expect(errorMessage).toBeInTheDocument();
      });
    });

    it('calls onSwitch when Log In link is clicked', () => {
      const switchLink = screen.getByText('Log In');
      fireEvent.click(switchLink);
      expect(mockSwitch).toHaveBeenCalled();
    });
  });
});
