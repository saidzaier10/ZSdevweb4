import api from './axios.js'

export const portfolioApi = {
  getProjects: () => api.get('/api/v1/portfolio/projects/'),
  getProject: (slug) => api.get(`/api/v1/portfolio/projects/${slug}/`),
  getTestimonials: () => api.get('/api/v1/portfolio/testimonials/'),
}
