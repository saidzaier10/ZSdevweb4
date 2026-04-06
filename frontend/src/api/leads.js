import api from './axios.js'

export const leadsApi = {
  capture: (data) => api.post('/api/v1/leads/', data),
}
