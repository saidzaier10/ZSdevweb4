import api from './axios.js'

export const quotesApi = {
  create: (data) => api.post('/api/v1/quotes/', data),
  getByUuid: (uuid) => api.get(`/api/v1/quotes/${uuid}/`),
  send: (uuid) => api.post(`/api/v1/quotes/${uuid}/send/`),
  getPdfUrl: (uuid) => `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/quotes/${uuid}/pdf/`,
  pricePreview: (data) => api.post('/api/v1/quotes/price-preview/', data),
}
