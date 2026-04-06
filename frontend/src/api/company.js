import api from './axios.js'

export const companyApi = {
  getSettings: () => api.get('/api/v1/company/settings/'),
}
