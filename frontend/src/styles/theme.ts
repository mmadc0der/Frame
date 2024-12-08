import { createGlobalStyle } from 'styled-components'

export const theme = {
  colors: {
    primary: '#2D3250',
    secondary: '#424769',
    accent: '#7077A1',
    background: '#F6B17A',
    text: '#2D3250'
  },
  fonts: {
    heading: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    body: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
  },
  breakpoints: {
    mobile: '320px',
    tablet: '768px',
    desktop: '1024px'
  },
  button: {
    primary: {
      background: 'transparent',
      color: '#2D3250',
      border: '2px solid #2D3250',
      transition: 'all 0.3s ease',
      '&:hover': {
        background: '#2D3250',
        color: '#F6B17A',
        borderColor: '#2D3250'
      },
      '&:active': {
        background: '#424769',
        color: '#F6B17A',
        outline: 'none',
        boxShadow: 'none'
      },
      '&:focus': {
        outline: 'none',
        boxShadow: 'none'
      }
    },
    secondary: {
      background: 'transparent',
      color: '#2D3250',
      border: '2px solid #2D3250',
      transition: 'all 0.3s ease',
      '&:hover': {
        background: '#2D3250',
        color: '#F6B17A',
        borderColor: '#2D3250'
      },
      '&:active': {
        background: '#424769',
        color: '#F6B17A',
        outline: 'none',
        boxShadow: 'none'
      },
      '&:focus': {
        outline: 'none',
        boxShadow: 'none'
      }
    }
  },
  landingPage: {
    container: {
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column'
    },
    header: {
      position: 'fixed',
      top: '0',
      left: '0',
      width: '100%',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '1rem 2rem',
      zIndex: 1000
    },
    logo: {
      fontFamily: 'fonts.heading',
      fontSize: '1.5rem',
      fontWeight: 'bold'
    },
    loginButton: {
      padding: '0.5rem 1rem',
      background: 'transparent',
      border: '2px solid colors.primary',
      color: 'colors.primary',
      borderRadius: '8px'
    },
    content: {
      flexGrow: 1,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    },
    centeredText: {
      textAlign: 'center',
      fontSize: '3rem',
      fontFamily: 'fonts.heading'
    },
    description: {
      maxWidth: '600px',
      textAlign: 'center',
      fontSize: '1.2rem'
    }
  }
}

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: ${props => props.theme.fonts.body};
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.text};
  }
`
