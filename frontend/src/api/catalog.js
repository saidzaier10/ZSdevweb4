import api from './axios.js'

export const catalogApi = {
  getCategories: () => api.get('/api/v1/catalog/categories/'),
  getProjectTypes: () => api.get('/api/v1/catalog/project-types/'),
  getDesignOptions: () => api.get('/api/v1/catalog/design-options/'),
  getComplexityLevels: () => api.get('/api/v1/catalog/complexity/'),
  getSupplementaryOptions: () => api.get('/api/v1/catalog/options/'),
}
