import api from './axios.js'

export const contactApi = {
  send: (data) => api.post('/api/v1/contacts/', data),
}
