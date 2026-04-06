import api from './axios.js'

export const authApi = {
  login: (email, password) => api.post('/api/v1/auth/token/', { email, password }),
  refresh: (refresh) => api.post('/api/v1/auth/token/refresh/', { refresh }),
  me: () => api.get('/api/v1/auth/me/'),
}
