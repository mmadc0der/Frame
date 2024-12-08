import { useState } from 'react';
import styled from 'styled-components';
import { AnimatePresence, motion } from 'framer-motion';
import { LoginForm } from './LoginForm';
import { RegisterForm } from './RegisterForm';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const Overlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: ${props => props.theme.zIndex.modal};
`;

const ModalContainer = styled(motion.div)`
  background: white;
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  position: relative;
  margin: 1rem;
`;

const Title = styled.h2`
  text-align: center;
  margin-bottom: 2rem;
  color: ${props => props.theme.colors.primary};
  font-family: ${props => props.theme.fonts.heading};
  font-weight: 600;
`;

const CloseButton = styled.button`
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: ${props => props.theme.colors.primary};
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  transition: background 0.2s;

  &:hover {
    background: ${props => props.theme.colors.modal.input};
  }
`;

export const AuthModal = ({ isOpen, onClose }: AuthModalProps) => {
  const [isLogin, setIsLogin] = useState(false);

  const handleSwitch = () => {
    setIsLogin(!isLogin);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <Overlay
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <ModalContainer
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ type: "spring", duration: 0.3 }}
            onClick={e => e.stopPropagation()}
          >
            <CloseButton onClick={onClose}>×</CloseButton>
            <Title>{isLogin ? 'Welcome Back' : 'Create Account'}</Title>

            {isLogin ? (
              <LoginForm onSwitch={handleSwitch} />
            ) : (
              <RegisterForm onSwitch={handleSwitch} />
            )}
          </ModalContainer>
        </Overlay>
      )}
    </AnimatePresence>
  );
};
