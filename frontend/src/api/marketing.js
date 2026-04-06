import api from './axios.js'

export const marketingApi = {
  getFaq: () => api.get('/api/v1/marketing/faq/'),
}
