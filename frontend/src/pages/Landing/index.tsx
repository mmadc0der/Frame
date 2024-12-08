import { useState, useEffect } from 'react'
import styled from 'styled-components'
import { motion } from 'framer-motion'

const Container = styled.div`
  min-height: 200vh;
  width: 100%;
  background-color: ${({ theme }) => theme.colors.background};
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
`

const Header = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: ${({ theme }) => theme.colors.primary};
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  z-index: 1000;
`

const Logo = styled.a`
  color: ${({ theme }) => theme.colors.text};
  text-decoration: none;
  font-size: 24px;
  font-weight: bold;

  &:hover {
    color: ${({ theme }) => theme.colors.accent};
  }
`

const LoginButton = styled.button`
  background-color: transparent;
  color: ${({ theme }) => theme.colors.text};
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
  transition: color 0.2s;

  &:hover {
    color: ${({ theme }) => theme.colors.accent};
  }
`

const Content = styled.main`
  margin-top: 60px;
  padding: 40px 20px;
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
`

const Title = styled(motion.h1)`
  font-size: 48px;
  color: ${({ theme }) => theme.colors.text};
  text-align: center;
  margin: 0;
`

const Description = styled(motion.p)`
  font-size: 24px;
  color: ${({ theme }) => theme.colors.text};
  text-align: center;
  max-width: 800px;
  margin: 0;
  opacity: 0;
`

const Footer = styled(motion.footer)`
  position: fixed;
  bottom: 20px;
  right: 20px;
  color: ${({ theme }) => theme.colors.text};
  font-size: 14px;
  opacity: 0.7;
`

export const Landing = () => {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <Container>
      <Header>
        <Logo href="/">Frame</Logo>
        <LoginButton>Log In</LoginButton>
      </Header>

      <Content>
        <Title
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          Welcome to Frame
        </Title>

        <Description
          initial={{ opacity: 0 }}
          animate={{ opacity: scrollY > window.innerHeight * 0.3 ? 1 : 0 }}
          transition={{ duration: 0.5 }}
        >
          Your creative space for amazing projects
        </Description>
      </Content>

      <Footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.7 }}
        transition={{ duration: 0.2 }}
      >
       &copy; created by madc0der
      </Footer>
    </Container>
  )
}
