import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import { FaHome, FaBrain, FaFileAlt, FaRobot, FaBars, FaTimes } from 'react-icons/fa';

const Nav = styled(motion.nav)`
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  padding: 10px 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
`;

const NavContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    position: fixed;
    top: 0;
    right: ${({ isOpen }) => (isOpen ? '0' : '-100%')};
    width: 250px;
    height: 100vh;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 80px 20px;
    transition: right 0.3s ease;
    border-radius: 20px 0 0 20px;
  }
`;

const NavLink = styled(Link)`
  color: ${({ active }) => (active ? '#ffd700' : 'white')};
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #ffd700;
  }
  
  @media (max-width: 768px) {
    color: ${({ active }) => (active ? '#ffd700' : '#333')};
  }
`;

const MenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  
  @media (max-width: 768px) {
    display: block;
  }
`;

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const links = [
    { to: '/', icon: <FaHome />, text: 'Home' },
    { to: '/predict', icon: <FaBrain />, text: 'Job Prediction' },
    { to: '/resume', icon: <FaFileAlt />, text: 'Resume Analysis' },
    { to: '/chatbot', icon: <FaRobot />, text: 'Chatbot' },
  ];

  return (
    <Nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', stiffness: 100 }}
    >
      <MenuButton onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? <FaTimes /> : <FaBars />}
      </MenuButton>
      
      <NavContainer isOpen={isOpen}>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            active={location.pathname === link.to ? 1 : 0}
            onClick={() => setIsOpen(false)}
          >
            {link.icon}
            <span>{link.text}</span>
          </NavLink>
        ))}
      </NavContainer>
    </Nav>
  );
}

export default Navbar;