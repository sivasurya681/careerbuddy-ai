import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styled from 'styled-components';
import axios from 'axios';
import { FaRobot, FaUser, FaPaperPlane, FaSpinner } from 'react-icons/fa';

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

const ChatContainer = styled(motion.div)`
  max-width: 800px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const MessagesContainer = styled.div`
  height: 500px;
  overflow-y: auto;
  padding: 20px;
  
  &::-webkit-scrollbar {
    width: 5px;
  }
  
  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 5px;
  }
`;

const MessageWrapper = styled(motion.div)`
  display: flex;
  margin-bottom: 1rem;
  justify-content: ${({ isUser }) => (isUser ? 'flex-end' : 'flex-start')};
`;

const Message = styled.div`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 20px;
  background: ${({ isUser }) =>
    isUser ? 'linear-gradient(45deg, #667eea, #764ba2)' : 'rgba(255, 255, 255, 0.2)'};
  color: white;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  
  svg {
    margin-top: 3px;
  }
`;

const MessageContent = styled.div`
  p {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-word;
  }
  
  ul, ol {
    margin: 5px 0;
    padding-left: 20px;
  }
  
  li {
    margin: 2px 0;
  }
`;

const InputContainer = styled.div`
  display: flex;
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.2);
`;

const Input = styled.input`
  flex: 1;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  margin-right: 10px;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }
  
  &:focus {
    outline: none;
    border-color: #ffd700;
  }
`;

const SendButton = styled(motion.button)`
  padding: 12px 20px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  gap: 5px;
  padding: 10px;
  
  span {
    width: 8px;
    height: 8px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    display: inline-block;
  }
`;

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: [{ type: 'text', content: 'Hello! I\'m your Career Assistant. How can I help you today?' }]
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { type: 'user', content: [{ type: 'text', content: userMessage }] }]);
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        query: userMessage
      });

      if (response.data.success) {
        setMessages(prev => [...prev, { type: 'bot', content: response.data.responses }]);
      } else {
        setMessages(prev => [...prev, { 
          type: 'bot', 
          content: [{ type: 'text', content: 'Sorry, I encountered an error.' }] 
        }]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { 
        type: 'bot', 
        content: [{ type: 'text', content: 'Sorry, I encountered an error. Please try again.' }] 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const renderMessage = (message) => {
    if (message.type === 'user') {
      return (
        <MessageWrapper isUser>
          <Message isUser>
            <FaUser />
            <MessageContent>
              <p>{message.content[0]?.content}</p>
            </MessageContent>
          </Message>
        </MessageWrapper>
      );
    }

    // Bot message - simple rendering without markdown
    return (
      <MessageWrapper>
        <Message>
          <FaRobot />
          <MessageContent>
            {message.content.map((item, index) => {
              if (item.type === 'heading') {
                return <h4 key={index}>{item.content}</h4>;
              } else if (item.type === 'bullet') {
                return <li key={index}>{item.content}</li>;
              } else {
                return <p key={index}>{item.content}</p>;
              }
            })}
          </MessageContent>
        </Message>
      </MessageWrapper>
    );
  };

  return (
    <Container>
      <Title
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Career Chatbot
      </Title>

      <ChatContainer
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <MessagesContainer>
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
              >
                {renderMessage(message)}
              </motion.div>
            ))}
          </AnimatePresence>
          
          {loading && (
            <MessageWrapper>
              <Message>
                <FaRobot />
                <TypingIndicator
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  <span />
                  <span />
                  <span />
                </TypingIndicator>
              </Message>
            </MessageWrapper>
          )}
          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputContainer>
          <Input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about careers, jobs, skills..."
            disabled={loading}
          />
          <SendButton
            onClick={handleSend}
            disabled={loading || !input.trim()}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {loading ? <FaSpinner className="spin" /> : <FaPaperPlane />}
            Send
          </SendButton>
        </InputContainer>
      </ChatContainer>
    </Container>
  );
}

export default Chatbot;