import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import { AccountCircle, Assignment } from '@mui/icons-material';
import Navbar from '../components/Navbar';
import { userAPI } from '../services/api';

function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [testResults, setTestResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    loadProfile();
    loadTestResults();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await userAPI.getProfile();
      setProfile(response.data.user);
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTestResults = async () => {
    try {
      const response = await userAPI.getTestResults();
      setTestResults(response.data.results);
    } catch (error) {
      console.error('Error loading test results:', error);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      await userAPI.updateProfile({
        interests: profile.profile.interests,
        career_preferences: profile.profile.career_preferences,
      });
      setMessage({ type: 'success', text: 'Cập nhật hồ sơ thành công!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Có lỗi xảy ra. Vui lòng thử lại.' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flex: 1 }}>
          <CircularProgress />
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      
      <Container maxWidth="lg" sx={{ py: 4, flex: 1 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
          👤 Hồ sơ cá nhân
        </Typography>

        {message.text && (
          <Alert severity={message.type} sx={{ mb: 3 }}>
            {message.text}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* Profile Info */}
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <AccountCircle sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
                <Typography variant="h6">Thông tin cá nhân</Typography>
              </Box>

              <TextField
                fullWidth
                label="Tên đăng nhập"
                value={profile?.username || ''}
                disabled
                margin="normal"
              />
              <TextField
                fullWidth
                label="Email"
                value={profile?.email || ''}
                disabled
                margin="normal"
              />
              <TextField
                fullWidth
                label="Họ và tên"
                value={profile?.full_name || ''}
                disabled
                margin="normal"
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Ngày tham gia: {profile?.created_at ? new Date(profile.created_at).toLocaleDateString('vi-VN') : 'N/A'}
              </Typography>
            </Paper>
          </Grid>

          {/* Test Results */}
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Assignment sx={{ fontSize: 40, mr: 2, color: 'secondary.main' }} />
                <Typography variant="h6">Kết quả bài test</Typography>
              </Box>

              {testResults.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  Bạn chưa làm bài test nào. Hãy thử làm bài test để tìm nghề phù hợp!
                </Typography>
              ) : (
                <Box>
                  {testResults.slice(0, 3).map((result, index) => (
                    <Card key={index} sx={{ mb: 2 }}>
                      <CardContent>
                        <Typography variant="subtitle2" gutterBottom>
                          Bài test: {result.test_type}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Ngày làm: {new Date(result.created_at).toLocaleDateString('vi-VN')}
                        </Typography>
                        {result.recommendations && result.recommendations.length > 0 && (
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="caption" gutterBottom>
                              Nghề được gợi ý:
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                              {result.recommendations.slice(0, 2).map((rec, idx) => (
                                <Chip
                                  key={idx}
                                  label={rec.career_name}
                                  size="small"
                                  color="primary"
                                />
                              ))}
                            </Box>
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>

        <Paper elevation={2} sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            📊 Thống kê hoạt động
          </Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={4}>
              <Card sx={{ backgroundColor: '#e3f2fd' }}>
                <CardContent>
                  <Typography variant="h4" align="center">
                    {testResults.length}
                  </Typography>
                  <Typography variant="body2" align="center" color="text.secondary">
                    Bài test đã làm
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Card sx={{ backgroundColor: '#fff3e0' }}>
                <CardContent>
                  <Typography variant="h4" align="center">
                    {profile?.profile?.interests?.length || 0}
                  </Typography>
                  <Typography variant="body2" align="center" color="text.secondary">
                    Sở thích
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Card sx={{ backgroundColor: '#e8f5e9' }}>
                <CardContent>
                  <Typography variant="h4" align="center">
                    {profile?.profile?.career_preferences?.length || 0}
                  </Typography>
                  <Typography variant="body2" align="center" color="text.secondary">
                    Nghề quan tâm
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </Box>
  );
}

export default ProfilePage;
