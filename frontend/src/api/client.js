import api from './axios.js'

export const clientApi = {
  getProjects: () => api.get('/client/projects/'),
  getProject: (uuid) => api.get(`/client/projects/${uuid}/`),
}
