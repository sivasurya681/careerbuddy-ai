import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import styled from 'styled-components';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import JobPrediction from './pages/JobPrediction';
import ResumeAnalysis from './pages/ResumeAnalysis';
import Chatbot from './pages/Chatbot';
import ThreeDBackground from './components/ThreeDBackground';
import './App.css';

const AppContainer = styled.div`
  min-height: 100vh;
  position: relative;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const ContentContainer = styled(motion.div)`
  position: relative;
  z-index: 2;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
`;

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setLoading(false), 2000);
  }, []);

  if (loading) {
    return (
      <div className="loading-screen">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 360],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
          }}
          className="loading-logo"
        >
          🚀
        </motion.div>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          CareerBuddy AI
        </motion.h1>
      </div>
    );
  }

  return (
    <Router>
      <AppContainer>
        <ThreeDBackground />
        <Navbar />
        <ContentContainer
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/predict" element={<JobPrediction />} />
              <Route path="/resume" element={<ResumeAnalysis />} />
              <Route path="/chatbot" element={<Chatbot />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </AnimatePresence>
        </ContentContainer>
      </AppContainer>
    </Router>
  );
}

export default App;