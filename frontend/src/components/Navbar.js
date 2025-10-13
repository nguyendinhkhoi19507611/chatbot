import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  AccountCircle,
  Chat,
  Work,
  Assignment,
  AdminPanelSettings,
  Logout,
} from '@mui/icons-material';
import { removeTokens, getUser } from '../utils/auth';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const user = getUser();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    removeTokens();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <AppBar position="static" elevation={2}>
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 0, mr: 4, fontWeight: 'bold', cursor: 'pointer' }}
          onClick={() => navigate('/chat')}
        >
          🤖 Career Chatbot
        </Typography>

        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          <Button
            color="inherit"
            startIcon={<Chat />}
            onClick={() => navigate('/chat')}
            sx={{
              backgroundColor: isActive('/chat') ? 'rgba(255,255,255,0.2)' : 'transparent',
            }}
          >
            Chat
          </Button>
          <Button
            color="inherit"
            startIcon={<Work />}
            onClick={() => navigate('/careers')}
            sx={{
              backgroundColor: isActive('/careers') ? 'rgba(255,255,255,0.2)' : 'transparent',
            }}
          >
            Nghề nghiệp
          </Button>
          <Button
            color="inherit"
            startIcon={<Assignment />}
            onClick={() => navigate('/test')}
            sx={{
              backgroundColor: isActive('/test') ? 'rgba(255,255,255,0.2)' : 'transparent',
            }}
          >
            Bài test
          </Button>
          {user?.role === 'admin' && (
            <Button
              color="inherit"
              startIcon={<AdminPanelSettings />}
              onClick={() => navigate('/admin')}
              sx={{
                backgroundColor: isActive('/admin') ? 'rgba(255,255,255,0.2)' : 'transparent',
              }}
            >
              Quản trị
            </Button>
          )}
        </Box>

        <Box>
          <IconButton
            size="large"
            onClick={handleMenu}
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem disabled>
              <Typography variant="body2" color="text.secondary">
                {user?.username || 'User'}
              </Typography>
            </MenuItem>
            <MenuItem onClick={() => { handleClose(); navigate('/profile'); }}>
              <AccountCircle sx={{ mr: 1 }} fontSize="small" />
              Hồ sơ
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <Logout sx={{ mr: 1 }} fontSize="small" />
              Đăng xuất
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
