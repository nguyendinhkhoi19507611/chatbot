import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Button,
  RadioGroup,
  FormControlLabel,
  Radio,
  LinearProgress,
  Card,
  CardContent,
  Grid,
  Chip,
  Alert,
} from '@mui/material';
import { Assignment, CheckCircle } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { userAPI } from '../services/api';

function TestPage() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const response = await userAPI.getTestQuestions('interest');
      setQuestions(response.data.questions);
    } catch (error) {
      console.error('Error loading questions:', error);
      setError('Không thể tải bài test. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, value) => {
    setAnswers({
      ...answers,
      [questionId]: value,
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = async () => {
    // Check if all questions are answered
    const unanswered = questions.filter(q => !answers[q.id]);
    if (unanswered.length > 0) {
      setError('Vui lòng trả lời tất cả các câu hỏi.');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      const formattedAnswers = questions.map(q => ({
        question_id: q.id,
        value: answers[q.id],
      }));

      const response = await userAPI.submitTest({
        test_type: 'interest',
        answers: formattedAnswers,
      });

      setResult(response.data.results);
    } catch (error) {
      console.error('Error submitting test:', error);
      setError('Có lỗi xảy ra khi nộp bài. Vui lòng thử lại.');
    } finally {
      setSubmitting(false);
    }
  };

  const progress = questions.length > 0 ? ((currentQuestion + 1) / questions.length) * 100 : 0;
  const currentQ = questions[currentQuestion];

  if (loading) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flex: 1 }}>
          <Typography>Đang tải bài test...</Typography>
        </Box>
      </Box>
    );
  }

  if (result) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <Container maxWidth="md" sx={{ py: 4, flex: 1 }}>
          <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
            <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
              Hoàn thành bài test!
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Dựa trên câu trả lời của bạn, chúng tôi đã phân tích sở thích và đề xuất các nghề nghiệp phù hợp.
            </Typography>

            {result.recommendations && result.recommendations.length > 0 && (
              <Box sx={{ mt: 4 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                  🎯 Nghề nghiệp được đề xuất:
                </Typography>
                <Grid container spacing={2} sx={{ mt: 2 }}>
                  {result.recommendations.map((rec, index) => (
                    <Grid item xs={12} key={index}>
                      <Card sx={{ textAlign: 'left', backgroundColor: '#f5f5f5' }}>
                        <CardContent>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                            <Typography variant="h6">
                              {index + 1}. {rec.career_name}
                            </Typography>
                            <Chip
                              label={`${(rec.confidence * 100).toFixed(0)}% phù hợp`}
                              color="primary"
                              size="small"
                            />
                          </Box>
                          <Typography variant="body2" color="text.secondary" paragraph>
                            {rec.description}
                          </Typography>
                          <Typography variant="body2">
                            💰 Mức lương: {rec.salary_range}
                          </Typography>
                          <Typography variant="body2">
                            🎓 Học vấn: {rec.education}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}

            <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button
                variant="outlined"
                onClick={() => window.location.reload()}
              >
                Làm lại bài test
              </Button>
              <Button
                variant="contained"
                onClick={() => navigate('/chat')}
              >
                Trò chuyện với Chatbot
              </Button>
            </Box>
          </Paper>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      
      <Container maxWidth="md" sx={{ py: 4, flex: 1 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Assignment sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
              Bài test đánh giá sở thích nghề nghiệp
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* Progress */}
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2" color="text.secondary">
                Câu hỏi {currentQuestion + 1} / {questions.length}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {progress.toFixed(0)}% hoàn thành
              </Typography>
            </Box>
            <LinearProgress variant="determinate" value={progress} />
          </Box>

          {/* Question */}
          {currentQ && (
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
                {currentQ.question}
              </Typography>
              <RadioGroup
                value={answers[currentQ.id] || ''}
                onChange={(e) => handleAnswerChange(currentQ.id, e.target.value)}
              >
                {currentQ.options.map((option) => (
                  <FormControlLabel
                    key={option.value}
                    value={option.value}
                    control={<Radio />}
                    label={option.label}
                    sx={{
                      border: '1px solid #e0e0e0',
                      borderRadius: 2,
                      mb: 1,
                      p: 1,
                      '&:hover': {
                        backgroundColor: '#f5f5f5',
                      },
                    }}
                  />
                ))}
              </RadioGroup>
            </Box>
          )}

          {/* Navigation */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              variant="outlined"
              onClick={handlePrevious}
              disabled={currentQuestion === 0}
            >
              Câu trước
            </Button>

            {currentQuestion === questions.length - 1 ? (
              <Button
                variant="contained"
                onClick={handleSubmit}
                disabled={submitting || !answers[currentQ?.id]}
              >
                {submitting ? 'Đang xử lý...' : 'Hoàn thành'}
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!answers[currentQ?.id]}
              >
                Câu tiếp theo
              </Button>
            )}
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}

export default TestPage;
