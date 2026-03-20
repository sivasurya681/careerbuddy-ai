import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styled from 'styled-components';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { FaUpload, FaLinkedin, FaSpinner, FaCheck, FaTimes } from 'react-icons/fa';

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

const DropzoneContainer = styled(motion.div)`
  max-width: 600px;
  margin: 0 auto 2rem;
  padding: 40px;
  border: 2px dashed ${({ isDragActive, hasFile }) => 
    hasFile ? '#4caf50' : isDragActive ? '#ffd700' : 'rgba(255, 255, 255, 0.3)'};
  border-radius: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
  
  &:hover {
    border-color: #ffd700;
  }
`;

const FileInfo = styled.div`
  margin-top: 1rem;
  padding: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
`;

const ResultsContainer = styled(motion.div)`
  max-width: 800px;
  margin: 0 auto;
`;

const SkillsSection = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 2rem;
`;

const SkillTag = styled.span`
  display: inline-block;
  padding: 5px 15px;
  background: rgba(255, 215, 0, 0.2);
  border: 1px solid #ffd700;
  border-radius: 20px;
  margin: 5px;
  color: white;
`;

const JobSection = styled.div`
  margin-bottom: 1.5rem;
`;

const JobSkill = styled.h3`
  color: #ffd700;
  margin-bottom: 1rem;
`;

function ResumeAnalysis() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const onDrop = useCallback((acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setResults(null);
    setError('');
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  });

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('resume', file);

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/parse-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (!response.data.error) {
        setResults(response.data);
      } else {
        setError(response.data.error);
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
        Resume Analysis
      </Title>

      <DropzoneContainer
        {...getRootProps()}
        isDragActive={isDragActive}
        hasFile={!!file}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        whileHover={{ scale: 1.02 }}
      >
        <input {...getInputProps()} />
        <FaUpload size={40} color={file ? '#4caf50' : 'rgba(255,255,255,0.5)'} />
        {file ? (
          <FileInfo>
            <FaCheck color="#4caf50" />
            <span>{file.name}</span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setFile(null);
              }}
              style={{ background: 'none', border: 'none', color: '#ff6b6b', cursor: 'pointer' }}
            >
              <FaTimes />
            </button>
          </FileInfo>
        ) : (
          <p>
            {isDragActive
              ? 'Drop your resume here'
              : 'Drag & drop your resume (PDF) here, or click to select'}
          </p>
        )}
      </DropzoneContainer>

      {file && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{ textAlign: 'center', marginBottom: '2rem' }}
        >
          <button
            onClick={handleUpload}
            disabled={loading}
            style={{
              padding: '15px 30px',
              background: 'linear-gradient(45deg, #667eea, #764ba2)',
              color: 'white',
              border: 'none',
              borderRadius: '10px',
              cursor: loading ? 'not-allowed' : 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '10px',
              fontSize: '1.1rem',
              opacity: loading ? 0.5 : 1
            }}
          >
            {loading ? <FaSpinner className="spin" /> : <FaUpload />}
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </motion.div>
      )}

      {error && (
        <p style={{ color: '#ff6b6b', textAlign: 'center' }}>{error}</p>
      )}

      <AnimatePresence>
        {results && (
          <ResultsContainer
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            {results.extracted_skills && results.extracted_skills.length > 0 && (
              <SkillsSection>
                <h2 style={{ marginBottom: '1rem', color: '#ffd700' }}>Extracted Skills</h2>
                <div>
                  {results.extracted_skills.map((skill, index) => (
                    <SkillTag key={index}>{skill}</SkillTag>
                  ))}
                </div>
              </SkillsSection>
            )}

            {results.matched_jobs && Object.keys(results.matched_jobs).length > 0 && (
              <SkillsSection>
                <h2 style={{ marginBottom: '1rem', color: '#ffd700' }}>Matched Jobs</h2>
                {Object.entries(results.matched_jobs).map(([skill, links], index) => (
                  <JobSection key={index}>
                    <JobSkill>{skill}</JobSkill>
                    {links.map((link, linkIndex) => (
                      <motion.a
                        key={linkIndex}
                        href={link}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '5px',
                          padding: '8px 15px',
                          margin: '5px',
                          background: 'rgba(0, 119, 181, 0.3)',
                          color: 'white',
                          textDecoration: 'none',
                          borderRadius: '5px',
                          border: '1px solid rgba(255, 255, 255, 0.2)'
                        }}
                        whileHover={{ y: -2 }}
                      >
                        <FaLinkedin /> LinkedIn Job {linkIndex + 1}
                      </motion.a>
                    ))}
                  </JobSection>
                ))}
              </SkillsSection>
            )}
          </ResultsContainer>
        )}
      </AnimatePresence>
    </Container>
  );
}

export default ResumeAnalysis;