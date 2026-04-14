import api from './axios.js'

export const authApi = {
  login:   (email, password) => api.post('/api/v1/auth/token/', { email, password }),
  refresh: () => api.post('/api/v1/auth/token/refresh/'),
  logout:  () => api.post('/api/v1/auth/logout/'),
  me:      () => api.get('/api/v1/auth/me/'),
  updateMe: (data) => api.patch('/api/v1/auth/me/', data),
  register: (data) => api.post('/api/v1/auth/register/', data),
  passwordResetRequest: (email) => api.post('/api/v1/auth/password-reset/', { email }),
  passwordResetConfirm: (data)  => api.post('/api/v1/auth/password-reset/confirm/', data),
  changePassword: (data) => api.post('/api/v1/auth/change-password/', data),
}
