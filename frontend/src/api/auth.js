import api from './axios.js'

export const authApi = {
  login: (email, password) => api.post('/api/v1/auth/token/', { email, password }),
  // Le refresh token est dans le cookie HttpOnly — pas de body nécessaire
  refresh: () => api.post('/api/v1/auth/token/refresh/'),
  logout: () => api.post('/api/v1/auth/logout/'),
  me: () => api.get('/api/v1/auth/me/'),
  register: (data) => api.post('/api/v1/auth/register/', data),
}
