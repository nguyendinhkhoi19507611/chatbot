import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Tabs,
  Tab,
} from '@mui/material';
import {
  People,
  Chat,
  Assignment,
  TrendingUp,
} from '@mui/icons-material';
import Navbar from '../components/Navbar';
import { adminAPI } from '../services/api';

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

function AdminPage() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, usersRes, convsRes] = await Promise.all([
        adminAPI.getStats(),
        adminAPI.getUsers(0, 20),
        adminAPI.getRecentConversations(50),
      ]);

      setStats(statsRes.data.stats);
      setUsers(usersRes.data.users);
      setConversations(convsRes.data.conversations);
    } catch (error) {
      console.error('Error loading admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
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
          🛠️ Quản trị hệ thống
        </Typography>

        {/* Statistics Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ backgroundColor: '#e3f2fd' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <People sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6">Người dùng</Typography>
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                  {stats?.total_users || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stats?.active_users || 0} hoạt động
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ backgroundColor: '#fff3e0' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Chat sx={{ mr: 1, color: 'warning.main' }} />
                  <Typography variant="h6">Cuộc trò chuyện</Typography>
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                  {stats?.total_conversations || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Tổng số tin nhắn
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ backgroundColor: '#e8f5e9' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Assignment sx={{ mr: 1, color: 'success.main' }} />
                  <Typography variant="h6">Bài test</Typography>
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                  {stats?.total_tests || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Đã hoàn thành
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ backgroundColor: '#fce4ec' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <TrendingUp sx={{ mr: 1, color: 'error.main' }} />
                  <Typography variant="h6">Tỷ lệ</Typography>
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                  {stats?.total_users > 0 
                    ? ((stats.active_users / stats.total_users) * 100).toFixed(0)
                    : 0}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Người dùng hoạt động
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Tabs */}
        <Paper elevation={2}>
          <Tabs value={tabValue} onChange={handleTabChange} sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tab label="Người dùng" />
            <Tab label="Cuộc trò chuyện" />
          </Tabs>

          {/* Users Tab */}
          <TabPanel value={tabValue} index={0}>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Tên đăng nhập</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell>Vai trò</TableCell>
                    <TableCell>Ngày tham gia</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {users.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>{user.username}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>
                        <Chip
                          label={user.role}
                          color={user.role === 'admin' ? 'error' : 'default'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        {user.created_at ? new Date(user.created_at).toLocaleDateString('vi-VN') : 'N/A'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>

          {/* Conversations Tab */}
          <TabPanel value={tabValue} index={1}>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Người dùng</TableCell>
                    <TableCell>Tin nhắn</TableCell>
                    <TableCell>Intent</TableCell>
                    <TableCell>Thời gian</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {conversations.map((conv) => (
                    <TableRow key={conv.id}>
                      <TableCell>{conv.user_id.substring(0, 8)}...</TableCell>
                      <TableCell sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {conv.message}
                      </TableCell>
                      <TableCell>
                        <Chip label={conv.intent || 'unknown'} size="small" />
                      </TableCell>
                      <TableCell>
                        {new Date(conv.timestamp).toLocaleString('vi-VN')}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </TabPanel>
        </Paper>
      </Container>
    </Box>
  );
}

export default AdminPage;
