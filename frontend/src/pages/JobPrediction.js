import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styled from 'styled-components';
import axios from 'axios';
import { FaSearch, FaLinkedin, FaSpinner } from 'react-icons/fa';

const Container = styled.div`
  min-height: 100vh;
  padding: 100px 20px 50px;
`;

const Title = styled(motion.h1)`
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 2rem;
  background: linear-gradient(45deg, #f3ec78, #af4261);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const InputContainer = styled(motion.div)`
  max-width: 600px;
  margin: 0 auto 2rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 15px 20px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: white;
  margin-bottom: 1rem;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }
  
  &:focus {
    outline: none;
    border-color: #ffd700;
  }
`;

const Button = styled(motion.button)`
  width: 100%;
  padding: 15px;
  font-size: 1.1rem;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const ResultsContainer = styled(motion.div)`
  max-width: 800px;
  margin: 0 auto;
`;

const JobCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const JobTitle = styled.h3`
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #ffd700;
`;

const Confidence = styled.div`
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 1rem;
`;

const LinksContainer = styled.div`
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
`;

const LinkButton = styled(motion.a)`
  padding: 8px 15px;
  background: rgba(0, 119, 181, 0.3);
  color: white;
  text-decoration: none;
  border-radius: 5px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  &:hover {
    background: rgba(0, 119, 181, 0.5);
  }
`;

function JobPrediction() {
  const [skills, setSkills] = useState('');
  const [role, setRole] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePredict = async () => {
    if (!skills) {
      setError('Please enter your skills');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/predict', {
        skills,
        role
      });

      if (response.data.success) {
        setPredictions(response.data.predictions);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Title
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Job Title Prediction
      </Title>

      <InputContainer
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Input
          type="text"
          placeholder="Enter your skills (e.g., Python, JavaScript, SQL)"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
        />
        <Input
          type="text"
          placeholder="Enter job role (optional)"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />
        <Button
          onClick={handlePredict}
          disabled={loading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? <FaSpinner className="spin" /> : <FaSearch />}
          {loading ? 'Predicting...' : 'Predict Job Titles'}
        </Button>
        {error && <p style={{ color: '#ff6b6b', marginTop: '1rem' }}>{error}</p>}
      </InputContainer>

      <AnimatePresence>
        {predictions.length > 0 && (
          <ResultsContainer
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {predictions.map((job, index) => (
              <JobCard
                key={index}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <JobTitle>{job.title}</JobTitle>
                <Confidence>Confidence: {(job.confidence * 100).toFixed(1)}%</Confidence>
                {job.linkedin_links && job.linkedin_links.length > 0 && (
                  <>
                    <p style={{ marginBottom: '0.5rem' }}>LinkedIn Jobs:</p>
                    <LinksContainer>
                      {job.linkedin_links.map((link, linkIndex) => (
                        <LinkButton
                          key={linkIndex}
                          href={link}
                          target="_blank"
                          rel="noopener noreferrer"
                          whileHover={{ y: -2 }}
                        >
                          <FaLinkedin /> Job {linkIndex + 1}
                        </LinkButton>
                      ))}
                    </LinksContainer>
                  </>
                )}
              </JobCard>
            ))}
          </ResultsContainer>
        )}
      </AnimatePresence>
    </Container>
  );
}

export default JobPrediction;