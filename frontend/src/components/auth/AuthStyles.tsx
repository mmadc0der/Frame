import styled from 'styled-components';

export interface InputProps {
  hasError?: boolean;
}

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
`;

export const Input = styled.input<InputProps>`
  padding: 0.875rem 1rem;
  background: ${props => props.theme.colors.modal.input};
  border: 2px solid ${props => props.hasError
    ? props.theme.colors.modal.error
    : props.theme.colors.modal.inputBorder};
  border-radius: 8px;
  font-family: ${props => props.theme.fonts.body};
  font-size: 1rem;
  width: 100%;
  transition: all 0.2s;
  color: ${props => props.theme.colors.primary};

  &:focus {
    outline: none;
    border-color: ${props => props.hasError
      ? props.theme.colors.modal.error
      : props.theme.colors.accent};
    box-shadow: 0 0 0 3px ${props => props.hasError
      ? props.theme.colors.modal.error + '20'
      : props.theme.colors.accent + '20'};
  }

  &::placeholder {
    color: #ADB5BD;
  }
`;

export const SubmitButton = styled.button`
  padding: 0.875rem;
  background: ${props => props.theme.colors.accent};
  color: white;
  border: none;
  border-radius: 8px;
  font-family: ${props => props.theme.fonts.body};
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: ${props => props.theme.colors.accentDark};
  }
`;

export const SocialButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.875rem;
  background: white;
  color: ${props => props.theme.colors.primary};
  border: 1px solid ${props => props.theme.colors.modal.inputBorder};
  border-radius: 8px;
  font-family: ${props => props.theme.fonts.body};
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: ${props => props.theme.colors.modal.input};
    border-color: ${props => props.theme.colors.primary};
  }
`;

export const Divider = styled.div`
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.5rem 0;
  color: ${props => props.theme.colors.primary};
  font-size: 0.875rem;

  &::before,
  &::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid ${props => props.theme.colors.modal.inputBorder};
  }

  &::before {
    margin-right: 1rem;
  }

  &::after {
    margin-left: 1rem;
  }
`;

export const ErrorMessage = styled.span`
  color: ${props => props.theme.colors.modal.error};
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
`;
