import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  TextField,
  InputAdornment,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
} from '@mui/material';
import { Search, Work } from '@mui/icons-material';
import Navbar from '../components/Navbar';
import { careerAPI } from '../services/api';

function CareersPage() {
  const [careers, setCareers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    loadCareers();
  }, []);

  const loadCareers = async () => {
    try {
      const response = await careerAPI.getAll();
      setCareers(response.data.careers);
    } catch (error) {
      console.error('Error loading careers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadCareers();
      return;
    }

    setLoading(true);
    try {
      const response = await careerAPI.search(searchQuery);
      setCareers(response.data.careers);
    } catch (error) {
      console.error('Error searching careers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = (career) => {
    setSelectedCareer(career);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedCareer(null);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      
      <Container maxWidth="lg" sx={{ py: 4, flex: 1 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
          💼 Danh sách nghề nghiệp
        </Typography>

        {/* Search */}
        <Box sx={{ mb: 4 }}>
          <TextField
            fullWidth
            placeholder="Tìm kiếm nghề nghiệp..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
              endAdornment: (
                <Button onClick={handleSearch}>Tìm kiếm</Button>
              ),
            }}
          />
        </Box>

        {/* Careers Grid */}
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            {careers.map((career) => (
              <Grid item xs={12} sm={6} md={4} key={career.id}>
                <Card
                  className="card-hover"
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                  }}
                >
                  <CardContent sx={{ flex: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Work color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6" component="div">
                        {career.name}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {career.description}
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 1 }}>
                      💰 {career.salary_range}
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {career.interests.slice(0, 3).map((interest, idx) => (
                        <Chip key={idx} label={interest} size="small" />
                      ))}
                    </Box>
                  </CardContent>
                  <CardActions>
                    <Button size="small" onClick={() => handleViewDetails(career)}>
                      Xem chi tiết
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}

        {!loading && careers.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h6" color="text.secondary">
              Không tìm thấy nghề nghiệp nào
            </Typography>
          </Box>
        )}
      </Container>

      {/* Career Detail Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        {selectedCareer && (
          <>
            <DialogTitle>
              <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {selectedCareer.name}
              </Typography>
            </DialogTitle>
            <DialogContent dividers>
              <Typography variant="body1" paragraph>
                <strong>Mô tả:</strong> {selectedCareer.description}
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>💰 Mức lương:</strong> {selectedCareer.salary_range}
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>🎓 Học vấn:</strong> {selectedCareer.education}
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>📈 Lộ trình phát triển:</strong>
              </Typography>
              <Typography variant="body2" sx={{ ml: 2, mb: 2 }}>
                {selectedCareer.career_path}
              </Typography>
              <Typography variant="body1" paragraph>
                <strong>💡 Sở thích phù hợp:</strong>
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {selectedCareer.interests.map((interest, idx) => (
                  <Chip key={idx} label={interest} color="primary" />
                ))}
              </Box>
              <Typography variant="body1" paragraph>
                <strong>⚡ Kỹ năng cần thiết:</strong>
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {selectedCareer.skills.map((skill, idx) => (
                  <Chip key={idx} label={skill} color="secondary" />
                ))}
              </Box>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Đóng</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
}

export default CareersPage;
