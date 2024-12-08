import { useState, useEffect } from 'react'
import styled from 'styled-components'
import { motion } from 'framer-motion'
import { AuthModal } from '../../components/auth/AuthModal'

const Container = styled.div`
  min-height: 200vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  background: ${props => props.theme.colors.background};
`

const Header = styled(motion.header)`
  position: ${props => props.theme.landingPage.header.position};
  top: ${props => props.theme.landingPage.header.top};
  left: ${props => props.theme.landingPage.header.left};
  width: ${props => props.theme.landingPage.header.width};
  display: ${props => props.theme.landingPage.header.display};
  justify-content: ${props => props.theme.landingPage.header.justifyContent};
  align-items: ${props => props.theme.landingPage.header.alignItems};
  padding: ${props => props.theme.landingPage.header.padding};
  background: transparent;
  z-index: ${props => props.theme.landingPage.header.zIndex};
`

const Logo = styled(motion.a)`
  font-family: ${props => props.theme.fonts.heading};
  font-size: 1.5rem;
  font-weight: bold;
  color: ${props => props.theme.colors.primary};
  text-decoration: none;
  cursor: pointer;

  &:hover {
    opacity: 0.8;
    color: ${props => props.theme.colors.primary};
  }

  &:visited {
    color: ${props => props.theme.colors.primary};
  }
`

const LoginButton = styled.button`
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  color: ${props => props.theme.colors.primary};
  font-family: ${props => props.theme.fonts.body};
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    opacity: 0.8;
  }
&:focus {
    outline: none;
    box-shadow: none;
  }
`

const Content = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
`

const CenteredText = styled(motion.div)`
  position: absolute;
  text-align: center;
  font-size: 4rem;
  font-weight: bold;
  font-family: ${props => props.theme.fonts.heading};
  color: ${props => props.theme.colors.primary};
  width: 100%;
  max-width: 800px;
  line-height: 1.2;
  padding: 0 2rem;
`

const Description = styled(motion.div)`
  position: absolute;
  text-align: center;
  font-size: 2rem;
  font-family: ${props => props.theme.fonts.body};
  color: ${props => props.theme.colors.secondary};
  width: 100%;
  max-width: 600px;
  line-height: 1.5;
  padding: 0 2rem;
`

const Footer = styled(motion.div)`
  position: fixed;
  bottom: 2rem;
  left: 0;
  width: 100%;
  text-align: center;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: ${props => props.theme.colors.primary};
  opacity: 0.7;
`

export const Landing = () => {
  const [scrollProgress, setScrollProgress] = useState(0)
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight
      const progress = Math.min(Math.max(window.scrollY / scrollHeight, 0), 1)
      setScrollProgress(progress)
    }

    let ticking = false
    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          handleScroll()
          ticking = false
        })
        ticking = true
      }
    }

    window.addEventListener('scroll', onScroll)
    handleScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <Container>
      <Header
        initial={{ opacity: 0, y: -20 }}
        animate={{
          opacity: scrollProgress > 0.1 ? 1 : 0,
          y: scrollProgress > 0.1 ? 0 : -20
        }}
        transition={{ duration: 0.2 }}
      >
        <Logo href="/">Frame</Logo>
        <LoginButton onClick={() => setIsAuthModalOpen(true)}>Sign Up</LoginButton>
      </Header>

      <Content>
        <CenteredText
          initial={{ opacity: 1, y: 0 }}
          animate={{
            opacity: scrollProgress < 0.3 ? 1 : 0,
            y: scrollProgress < 0.3 ? 0 : -50
          }}
          transition={{
            duration: 0.2,
            ease: "easeOut"
          }}
        >
          Welcome to Frame
        </CenteredText>
        <Description
          initial={{ opacity: 0, y: 50 }}
          animate={{
            opacity: scrollProgress > 0.3 ? 1 : 0,
            y: scrollProgress > 0.3 ? 0 : 50
          }}
          transition={{
            duration: 0.2,
            ease: "easeOut"
          }}
        >
          Your creative space for amazing projects
        </Description>
      </Content>

      <Footer
        initial={{ opacity: 0 }}
        animate={{
          opacity: scrollProgress > 0.3 ? 0.7 : 0
        }}
        transition={{ duration: 0.2 }}
      >
       &copy; created by madc0der
      </Footer>

      <AuthModal 
        isOpen={isAuthModalOpen} 
        onClose={() => setIsAuthModalOpen(false)} 
      />
    </Container>
  )
}
