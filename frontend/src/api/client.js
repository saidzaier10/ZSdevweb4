import api from './axios.js'

export const clientApi = {
  getProjects: () => api.get('/api/v1/client/projects/'),
  getProject: (uuid) => api.get(`/api/v1/client/projects/${uuid}/`),
}
