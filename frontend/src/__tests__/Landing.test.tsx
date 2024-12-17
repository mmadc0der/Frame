import * as React from 'react';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import { ThemeProvider } from 'styled-components';
import { Landing } from '../pages/Landing';
import { theme } from '../styles/theme';

// Мокаем window.scrollY
Object.defineProperty(window, 'scrollY', {
  value: 0,
  writable: true
});

// Мокаем requestAnimationFrame
global.requestAnimationFrame = (callback) => setTimeout(callback, 0);

const renderWithTheme = (component: React.ReactNode) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('Landing Component', () => {
  beforeEach(() => {
    // Сбрасываем значение scrollY перед каждым тестом
    window.scrollY = 0;
  });

  afterEach(() => {
    cleanup();
  });

  it('renders initial welcome message', () => {
    renderWithTheme(<Landing />);
    const welcomeMessage = screen.getByText('Welcome to Frame');
    expect(welcomeMessage).toBeInTheDocument();
  });

  it('renders Frame logo that links to home', () => {
    renderWithTheme(<Landing />);
    const logos = screen.getAllByText('Frame');
    const hasLogoWithHomeLink = logos.some(logo => {
      const link = logo.closest('a');
      return link?.getAttribute('href') === '/';
    });
    expect(hasLogoWithHomeLink).toBe(true);
  });

  it('renders login button', () => {
    renderWithTheme(<Landing />);
    const loginButton = screen.getByText('Sign Up');
    expect(loginButton).toBeInTheDocument();
  });

  it('shows creator signature', () => {
    renderWithTheme(<Landing />);
    const signature = screen.getByText(/created by madc0der$/);
    expect(signature).toBeInTheDocument();
  });

  // Тест на анимацию при скролле
  it('handles scroll events', () => {
    renderWithTheme(<Landing />);

    // Эмулируем скролл
    fireEvent.scroll(window, { target: { scrollY: window.innerHeight * 0.4 } });

    // Проверяем, что описание появилось
    expect(screen.getByText('Your creative space for amazing projects')).toBeInTheDocument();
  });
});
