import React, { useState, useEffect, useRef } from 'react';
import {
  Container,
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Avatar,
  Grid,
} from '@mui/material';
import { Send, Person, SmartToy, DeleteOutline } from '@mui/icons-material';
import Navbar from '../components/Navbar';
import { chatbotAPI } from '../services/api';
import ReactMarkdown from 'react-markdown';

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    loadHistory();
    loadSuggestions();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadHistory = async () => {
    try {
      const response = await chatbotAPI.getHistory(0, 20);
      const history = response.data.conversations.reverse();
      setMessages(history);
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const loadSuggestions = async () => {
    try {
      const response = await chatbotAPI.getSuggestions();
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error loading suggestions:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setLoading(true);

    // Add user message immediately
    const tempMessage = {
      message: userMessage,
      response: '',
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempMessage]);

    try {
      const response = await chatbotAPI.sendMessage(userMessage);
      const botResponse = response.data;

      // Update with bot response
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          message: userMessage,
          response: botResponse.response,
          recommendations: botResponse.recommendations,
          timestamp: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          message: userMessage,
          response: 'Xin lỗi, có lỗi xảy ra. Vui lòng thử lại.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
  };

  const handleClearHistory = async () => {
    if (window.confirm('Bạn có chắc muốn xóa toàn bộ lịch sử trò chuyện?')) {
      try {
        await chatbotAPI.deleteHistory();
        setMessages([]);
      } catch (error) {
        console.error('Error clearing history:', error);
      }
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Navbar />
      
      <Container maxWidth="lg" sx={{ flex: 1, display: 'flex', flexDirection: 'column', py: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
            💬 Trò chuyện với AI Chatbot
          </Typography>
          <IconButton color="error" onClick={handleClearHistory} title="Xóa lịch sử">
            <DeleteOutline />
          </IconButton>
        </Box>

        {/* Suggestions */}
        {messages.length === 0 && suggestions.length > 0 && (
          <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              💡 Gợi ý câu hỏi:
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {suggestions.map((suggestion, index) => (
                <Chip
                  key={index}
                  label={suggestion}
                  onClick={() => handleSuggestionClick(suggestion)}
                  clickable
                  color="primary"
                  variant="outlined"
                />
              ))}
            </Box>
          </Paper>
        )}

        {/* Messages */}
        <Paper
          elevation={2}
          sx={{
            flex: 1,
            overflow: 'auto',
            p: 2,
            mb: 2,
            backgroundColor: '#f9f9f9',
          }}
        >
          {messages.length === 0 ? (
            <Box
              sx={{
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexDirection: 'column',
              }}
            >
              <SmartToy sx={{ fontSize: 80, color: '#ccc', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                Bắt đầu cuộc trò chuyện
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Hãy hỏi tôi về sở thích và nghề nghiệp của bạn
              </Typography>
            </Box>
          ) : (
            messages.map((msg, index) => (
              <Box key={index} sx={{ mb: 3 }}>
                {/* User Message */}
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', maxWidth: '70%' }}>
                    <Paper
                      sx={{
                        p: 2,
                        backgroundColor: '#2196f3',
                        color: 'white',
                        borderRadius: '18px 18px 4px 18px',
                      }}
                    >
                      <Typography variant="body1">{msg.message}</Typography>
                    </Paper>
                    <Avatar sx={{ ml: 1, bgcolor: '#2196f3' }}>
                      <Person />
                    </Avatar>
                  </Box>
                </Box>

                {/* Bot Response */}
                {msg.response && (
                  <Box sx={{ display: 'flex', justifyContent: 'flex-start' }}>
                    <Box sx={{ display: 'flex', alignItems: 'flex-start', maxWidth: '70%' }}>
                      <Avatar sx={{ mr: 1, bgcolor: '#ff9800' }}>
                        <SmartToy />
                      </Avatar>
                      <Paper
                        sx={{
                          p: 2,
                          backgroundColor: 'white',
                          borderRadius: '18px 18px 18px 4px',
                        }}
                      >
                        <ReactMarkdown>{msg.response}</ReactMarkdown>
                        
                        {/* Career Recommendations */}
                        {msg.recommendations && msg.recommendations.length > 0 && (
                          <Grid container spacing={1} sx={{ mt: 2 }}>
                            {msg.recommendations.slice(0, 3).map((rec, idx) => (
                              <Grid item xs={12} key={idx}>
                                <Card variant="outlined" sx={{ backgroundColor: '#f5f5f5' }}>
                                  <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
                                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                                      {rec.career_name}
                                    </Typography>
                                    <Typography variant="caption" color="text.secondary">
                                      Độ phù hợp: {(rec.confidence * 100).toFixed(0)}%
                                    </Typography>
                                  </CardContent>
                                </Card>
                              </Grid>
                            ))}
                          </Grid>
                        )}
                      </Paper>
                    </Box>
                  </Box>
                )}
              </Box>
            ))
          )}
          <div ref={messagesEndRef} />
        </Paper>

        {/* Input */}
        <Paper elevation={2} sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              placeholder="Nhập tin nhắn của bạn..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              disabled={loading}
              multiline
              maxRows={3}
            />
            <IconButton
              color="primary"
              onClick={handleSendMessage}
              disabled={loading || !inputMessage.trim()}
              sx={{ alignSelf: 'flex-end' }}
            >
              {loading ? <CircularProgress size={24} /> : <Send />}
            </IconButton>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}

export default ChatPage;
