import api from './axios.js'

export const auditApi = {
  request: (data) => api.post('/api/v1/audit/', data),
}
