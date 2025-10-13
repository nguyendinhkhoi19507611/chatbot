import jwtDecode from 'jwt-decode';

export const getToken = () => {
  return localStorage.getItem('access_token');
};

export const setToken = (token) => {
  localStorage.setItem('access_token', token);
};

export const getRefreshToken = () => {
  return localStorage.getItem('refresh_token');
};

export const setRefreshToken = (token) => {
  localStorage.setItem('refresh_token', token);
};

export const removeTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
};

export const isAuthenticated = () => {
  const token = getToken();
  if (!token) return false;
  
  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    
    if (decoded.exp < currentTime) {
      removeTokens();
      return false;
    }
    
    return true;
  } catch (error) {
    removeTokens();
    return false;
  }
};

export const getUserFromToken = () => {
  const token = getToken();
  if (!token) return null;
  
  try {
    return jwtDecode(token);
  } catch (error) {
    return null;
  }
};

export const setUser = (user) => {
  localStorage.setItem('user', JSON.stringify(user));
};

export const getUser = () => {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  
  try {
    return JSON.parse(userStr);
  } catch (error) {
    return null;
  }
};
