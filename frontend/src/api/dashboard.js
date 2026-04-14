import api from './axios.js'

export const dashboardApi = {
  getStats: () => api.get('/api/v1/quotes/dashboard/'),
}
