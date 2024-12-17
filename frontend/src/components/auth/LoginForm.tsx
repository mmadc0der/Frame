import { useState } from 'react';
import styled from 'styled-components';
import { Form, Input, SubmitButton, SocialButton, Divider, ErrorMessage } from './AuthStyles';
import { authService } from '../../services/auth';

interface LoginFormProps {
  onSwitch: () => void;
}

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

export const LoginForm = ({ onSwitch }: LoginFormProps) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [touched, setTouched] = useState<{ email: boolean; password: boolean }>({
    email: false,
    password: false
  });

  const validateEmail = (value: string) => {
    if (!value) {
      return 'Email is required';
    }
    if (!/\S+@\S+\.\S+/.test(value)) {
      return 'Email is invalid';
    }
    return '';
  };

  const validatePassword = (value: string) => {
    if (!value) {
      return 'Password is required';
    }
    if (value.length < 6) {
      return 'Password must be at least 6 characters';
    }
    return '';
  };

  const handleChange = (field: 'email' | 'password', value: string) => {
    const setters = {
      email: setEmail,
      password: setPassword
    };
    const validators = {
      email: validateEmail,
      password: validatePassword
    };

    setters[field](value);

    if (touched[field]) {
      const error = validators[field](value);
      setErrors(prev => ({ ...prev, [field]: error }));
    }
  };

  const handleBlur = (field: 'email' | 'password') => {
    setTouched(prev => ({ ...prev, [field]: true }));
    const validators = {
      email: validateEmail,
      password: validatePassword
    };
    const error = validators[field](field === 'email' ? email : password);
    setErrors(prev => ({ ...prev, [field]: error }));
  };

  const validateForm = () => {
    const emailError = validateEmail(email);
    const passwordError = validatePassword(password);

    setTouched({ email: true, password: true });
    setErrors({
      email: emailError,
      password: passwordError
    });

    return !emailError && !passwordError;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      try {
        await authService.login({ email, password });
        // TODO: Handle successful login (e.g., redirect, show message, etc.)
        console.log('Login successful');
      } catch (error) {
        setErrors({ email: 'Invalid email or password.' });
        setErrors({ password: ''});
      }
    }
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <div>
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => handleChange('email', e.target.value)}
            onBlur={() => handleBlur('email')}
            $hasError={touched.email && !!errors.email}
          />
          {touched.email && errors.email && <ErrorMessage>{errors.email}</ErrorMessage>}
        </div>

        <div>
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => handleChange('password', e.target.value)}
            onBlur={() => handleBlur('password')}
            $hasError={touched.password && !!errors.password}
          />
          {touched.password && errors.password && <ErrorMessage>{errors.password}</ErrorMessage>}
        </div>

        <SubmitButton type="submit">Log In</SubmitButton>
      </Form>

      <Divider>or</Divider>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        <SocialButton type="button"> {/* onClick={() => authService.loginWithYandex()} */}
          <svg viewBox="0 0 195.7 195.7" width="24" height="24" xmlns="http://www.w3.org/2000/svg">
            <path d="M81.2,1.4c19.3-3.4,39.6-0.8,57.4,7.4c21.2,9.6,38.6,27,48.2,48.1c9.6,20.5,11.4,44.5,5.6,66.3c-6.5,24.5-22.9,46.1-44.8,58.9c-22,13.1-49.3,16.8-74.2,10.4C50.6,186.8,30.1,172.5,17,153C2.9,132.5-2.8,106.5,1.3,82c3-18.5,11.4-36,24.1-49.9C39.8,16,59.8,5,81.2,1.4L81.2,1.4z M84.6,17.7C57.4,22,33.2,41.3,22.8,66.8c-8,18.9-8.3,41-0.8,60.1c8,21.2,25.4,38.7,46.6,46.7c18.2,7.2,39.1,7.3,57.4,0.5c21.1-7.7,38.6-24.6,47-45.4c6.5-15.5,7.8-33,4-49.3c-4.3-18.4-15.2-35.2-30.5-46.5C129.1,19.7,106.1,13.9,84.6,17.7L84.6,17.7zM71.1,55.1c9-9.1,22.3-11.7,34.6-12.1c9.9,0,19.8,0.1,29.7-0.1c0,36.6,0,73.1,0,109.7c-6.4,0-12.8,0-19.2,0c0-31.7,0-63.4,0-95.1c-9.5,0.1-20.2-1.2-28.1,5.2c-8,6.1-7.6,17.8-4.4,26.4c4.7,11.1,16.8,15.6,25.6,22.7c-9.5,13.4-18.4,27.2-27.8,40.8c-7.3-0.1-14.7-0.1-22-0.1c8.7-12.3,17.5-24.6,26.2-36.9c-8.8-6.4-18.1-13.6-21.6-24.4C60.5,79.1,62,64.5,71.1,55.1L71.1,55.1z" />
          </svg>
          Continue with Yandex
        </SocialButton>

        <SocialButton type="button"> {/* onClick={() => authService.loginWithGitHub()}> */}
          <svg viewBox="0 0 98 96" width="24" height="24">
            <path fillRule="evenodd" clipRule="evenodd" d="M48.854 0C21.839 0 0 22 0 49.217c0 21.756 13.993 40.172 33.405 46.69 2.427.49 3.316-1.059 3.316-2.362 0-1.141-.08-5.052-.08-9.127-13.59 2.934-16.42-5.867-16.42-5.867-2.184-5.704-5.42-7.17-5.42-7.17-4.448-3.015.324-3.015.324-3.015 4.934.326 7.523 5.052 7.523 5.052 4.367 7.496 11.404 5.378 14.235 4.074.404-3.178 1.699-5.378 3.074-6.6-10.839-1.141-22.243-5.378-22.243-24.283 0-5.378 1.94-9.778 5.014-13.2-.485-1.222-2.184-6.275.486-13.038 0 0 4.125-1.304 13.426 5.052a46.97 46.97 0 0 1 12.214-1.63c4.125 0 8.33.571 12.213 1.63 9.302-6.356 13.427-5.052 13.427-5.052 2.67 6.763.97 11.816.485 13.038 3.155 3.422 5.015 7.822 5.015 13.2 0 18.905-11.404 23.06-22.324 24.283 1.78 1.548 3.316 4.481 3.316 9.126 0 6.6-.08 11.897-.08 13.526 0 1.304.89 2.853 3.316 2.364 19.412-6.52 33.405-24.935 33.405-46.691C97.707 22 75.788 0 48.854 0z" fill="#24292f"/>
          </svg>
          Continue with GitHub
        </SocialButton>
      </div>

      <SwitchText>
        No account yet?{' '}
        <SwitchLink onClick={onSwitch}>Sign Up</SwitchLink>
      </SwitchText>
    </>
  );
};
